#!/usr/bin/env python3
"""
通用邮件发送工具
支持 Gmail、QQ、163、Outlook、飞书等主流邮箱
"""

import smtplib
import ssl
import os
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict


def load_env_file() -> bool:
    """加载 .env 文件"""
    env_paths = [
        Path.home() / ".openclaw" / ".env",
        Path.home() / ".openclaw" / "config" / "main.env",
        Path("/root/.openclaw/.env"),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        if key not in os.environ:
                            os.environ[key] = value
            return True
    return False


# 加载环境变量
load_env_file()

# SMTP 配置
SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('EMAIL_SENDER', '')
SMTP_PASSWORD = os.getenv('EMAIL_SMTP_PASSWORD', '')
USE_TLS = os.getenv('EMAIL_USE_TLS', 'true').lower() == 'true'

# 常见邮箱服务商配置
EMAIL_PROVIDERS = {
    'gmail': {
        'server': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'password_type': 'App Password'
    },
    'qq': {
        'server': 'smtp.qq.com',
        'port': 465,
        'use_tls': False,
        'password_type': '授权码'
    },
    '163': {
        'server': 'smtp.163.com',
        'port': 465,
        'use_tls': False,
        'password_type': '授权码'
    },
    'outlook': {
        'server': 'smtp.office365.com',
        'port': 587,
        'use_tls': True,
        'password_type': '邮箱密码'
    },
    'feishu': {
        'server': 'smtp.feishu.cn',
        'port': 465,
        'use_tls': False,
        'password_type': '邮箱密码'
    }
}


def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    password: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    use_tls: Optional[bool] = None
) -> Dict:
    """
    发送纯文本邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
        from_email: 发件人邮箱（可选，默认从环境变量读取）
        password: 邮箱密码/授权码（可选，默认从环境变量读取）
        smtp_server: SMTP服务器（可选）
        smtp_port: SMTP端口（可选）
        use_tls: 是否使用TLS（可选）
    
    Returns:
        {'success': bool, 'message': str}
    """
    sender = from_email or SENDER_EMAIL
    pwd = password or SMTP_PASSWORD
    server = smtp_server or SMTP_SERVER
    port = smtp_port or SMTP_PORT
    tls = use_tls if use_tls is not None else USE_TLS
    
    if not sender:
        return {'success': False, 'message': '未配置发件人邮箱，请设置 EMAIL_SENDER'}
    
    if not pwd:
        return {'success': False, 'message': '未配置邮箱密码，请设置 EMAIL_SMTP_PASSWORD'}
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 根据端口选择连接方式
        if port == 465:
            # SSL 连接
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(server, port, context=context) as s:
                s.login(sender, pwd)
                s.send_message(msg)
        else:
            # TLS 连接
            with smtplib.SMTP(server, port) as s:
                s.starttls()
                s.login(sender, pwd)
                s.send_message(msg)
        
        return {'success': True, 'message': f'邮件已发送至 {to_email}'}
        
    except Exception as e:
        error_msg = str(e)
        if 'authentication' in error_msg.lower():
            return {
                'success': False,
                'message': f'认证失败: 请检查邮箱地址和密码/授权码是否正确。{error_msg}'
            }
        elif 'UNEXPECTED_EOF' in error_msg or 'violation of protocol' in error_msg:
            return {
                'success': False,
                'message': 'SSL连接失败。请检查网络环境或SMTP配置。'
            }
        return {'success': False, 'message': f'发送失败: {error_msg}'}


def send_html_email(
    to_email: str,
    subject: str,
    html_body: str,
    from_email: Optional[str] = None,
    password: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    use_tls: Optional[bool] = None
) -> Dict:
    """
    发送HTML邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        html_body: HTML格式的邮件正文
        from_email: 发件人邮箱（可选）
        password: 邮箱密码/授权码（可选）
        smtp_server: SMTP服务器（可选）
        smtp_port: SMTP端口（可选）
        use_tls: 是否使用TLS（可选）
    
    Returns:
        {'success': bool, 'message': str}
    """
    sender = from_email or SENDER_EMAIL
    pwd = password or SMTP_PASSWORD
    server = smtp_server or SMTP_SERVER
    port = smtp_port or SMTP_PORT
    tls = use_tls if use_tls is not None else USE_TLS
    
    if not sender:
        return {'success': False, 'message': '未配置发件人邮箱'}
    
    if not pwd:
        return {'success': False, 'message': '未配置邮箱密码'}
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        if port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(server, port, context=context) as s:
                s.login(sender, pwd)
                s.send_message(msg)
        else:
            with smtplib.SMTP(server, port) as s:
                s.starttls()
                s.login(sender, pwd)
                s.send_message(msg)
        
        return {'success': True, 'message': f'HTML邮件已发送至 {to_email}'}
        
    except Exception as e:
        return {'success': False, 'message': f'发送失败: {str(e)}'}


def send_email_with_attachments(
    to_email: str,
    subject: str,
    body: str,
    attachments: List[tuple],
    is_html: bool = False,
    from_email: Optional[str] = None,
    password: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    use_tls: Optional[bool] = None
) -> Dict:
    """
    发送带附件的邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
        attachments: 附件列表 [(文件名, 文件路径), ...]
        is_html: 是否为HTML邮件
        from_email: 发件人邮箱（可选）
        password: 邮箱密码/授权码（可选）
        smtp_server: SMTP服务器（可选）
        smtp_port: SMTP端口（可选）
        use_tls: 是否使用TLS（可选）
    
    Returns:
        {'success': bool, 'message': str}
    """
    sender = from_email or SENDER_EMAIL
    pwd = password or SMTP_PASSWORD
    server = smtp_server or SMTP_SERVER
    port = smtp_port or SMTP_PORT
    tls = use_tls if use_tls is not None else USE_TLS
    
    if not sender or not pwd:
        return {'success': False, 'message': '未配置邮箱信息'}
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to_email
        msg['Subject'] = subject
        
        content_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, content_type, 'utf-8'))
        
        attached_count = 0
        for filename, filepath in attachments:
            if not os.path.exists(filepath):
                print(f"警告: 附件不存在，跳过: {filepath}")
                continue
            
            with open(filepath, 'rb') as f:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(f.read())
            
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            msg.attach(attachment)
            attached_count += 1
        
        if port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(server, port, context=context) as s:
                s.login(sender, pwd)
                s.send_message(msg)
        else:
            with smtplib.SMTP(server, port) as s:
                s.starttls()
                s.login(sender, pwd)
                s.send_message(msg)
        
        return {
            'success': True,
            'message': f'邮件已发送至 {to_email}（含{attached_count}个附件）'
        }
        
    except Exception as e:
        return {'success': False, 'message': f'发送失败: {str(e)}'}


def get_provider_config(email: str) -> Optional[Dict]:
    """根据邮箱地址自动识别服务商配置"""
    domain = email.split('@')[-1].lower()
    
    if 'gmail.com' in domain:
        return EMAIL_PROVIDERS['gmail']
    elif 'qq.com' in domain:
        return EMAIL_PROVIDERS['qq']
    elif '163.com' in domain:
        return EMAIL_PROVIDERS['163']
    elif 'outlook.com' in domain or 'hotmail.com' in domain or 'live.com' in domain:
        return EMAIL_PROVIDERS['outlook']
    elif 'feishu.cn' in domain:
        return EMAIL_PROVIDERS['feishu']
    
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='邮件发送工具')
    parser.add_argument('--to', required=True, help='收件人邮箱')
    parser.add_argument('--subject', required=True, help='邮件主题')
    parser.add_argument('--body', required=True, help='邮件正文')
    parser.add_argument('--html', action='store_true', help='发送HTML邮件')
    parser.add_argument('--attachments', help='附件路径，多个用逗号分隔')
    parser.add_argument('--from', dest='from_email', help='发件人邮箱')
    parser.add_argument('--password', help='邮箱密码/授权码')
    
    args = parser.parse_args()
    
    attachments = []
    if args.attachments:
        paths = args.attachments.split(',')
        attachments = [(os.path.basename(p.strip()), p.strip()) for p in paths]
    
    if attachments:
        result = send_email_with_attachments(
            to_email=args.to,
            subject=args.subject,
            body=args.body,
            attachments=attachments,
            is_html=args.html,
            from_email=args.from_email,
            password=args.password
        )
    elif args.html:
        result = send_html_email(
            to_email=args.to,
            subject=args.subject,
            html_body=args.body,
            from_email=args.from_email,
            password=args.password
        )
    else:
        result = send_email(
            to_email=args.to,
            subject=args.subject,
            body=args.body,
            from_email=args.from_email,
            password=args.password
        )
    
    print(result['message'])
    exit(0 if result['success'] else 1)
