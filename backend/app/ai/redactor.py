import re

class SensitiveDataRedactor:
    """Scrubs sensitive credentials and secrets before external AI calls."""
    
    @staticmethod
    def redact(text: str) -> str:
        if not text:
            return ""
            
        # Redact API Keys / Tokens
        redacted = re.sub(
            r'(api_key|secret|password|auth_token|jwt|bearer)\s*[:=]\s*["\'][A-Za-z0-9_\-]{8,}["\']',
            r'\1 = "[REDACTED_SECRET]"',
            text,
            flags=re.IGNORECASE
        )
        
        # Redact Emails
        redacted = re.sub(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "[REDACTED_EMAIL]",
            redacted
        )
        
        # Redact generic private key strings
        redacted = re.sub(
            r'-----BEGIN PRIVATE KEY-----[\s\S]*?-----END PRIVATE KEY-----',
            "[REDACTED_PRIVATE_KEY]",
            redacted
        )
        
        return redacted
