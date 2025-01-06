"""
Credential Manager Module
Handles secure storage and retrieval of credentials
"""
from cryptography.fernet import Fernet
import os
import base64
from flask import current_app

class CredentialManager:
    _instance = None
    _key = None
    _cipher_suite = None
    
    def __init__(self, app=None):
        """
        Initialize the Credential Manager
        
        Args:
            app: Flask application instance (optional)
        """
        if app:
            self.init_app(app)
            
    def init_app(self, app):
        """
        Initialize the application with the extension.
        
        Args:
            app: Flask application instance
        """
        if not self._key:
            self._key = self._get_or_create_key(app)
            self._cipher_suite = Fernet(self._key)
            
    @staticmethod
    def _get_or_create_key(app):
        """
        Get existing or create new encryption key
        
        Args:
            app: Flask application instance
            
        Returns:
            bytes: Encryption key
        """
        key_file = os.path.join(app.root_path, 'instance', 'crypto.key')
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_password(self, password):
        """
        Encrypt a password
        
        Args:
            password (str): Password to encrypt
            
        Returns:
            bytes: Encrypted password
        """
        if not self._cipher_suite:
            raise RuntimeError("CredentialManager not initialized with app context")
        return self._cipher_suite.encrypt(password.encode())
    
    def decrypt_password(self, encrypted_password):
        """
        Decrypt an encrypted password
        
        Args:
            encrypted_password (bytes): Encrypted password to decrypt
            
        Returns:
            str: Decrypted password
        """
        if not self._cipher_suite:
            raise RuntimeError("CredentialManager not initialized with app context")
        return self._cipher_suite.decrypt(encrypted_password).decode()
    
    def get_ps_credential_script(self, username, encrypted_password):
        """
        Generate PowerShell script for secure credential creation
        
        Args:
            username (str): Username for the credential
            encrypted_password (bytes): Encrypted password
            
        Returns:
            str: PowerShell script for credential creation
        """
        if not self._cipher_suite:
            raise RuntimeError("CredentialManager not initialized with app context")
        decrypted_password = self.decrypt_password(encrypted_password)
        return f"""
        $securePass = ConvertTo-SecureString "{decrypted_password}" -AsPlainText -Force
        $cred = New-Object System.Management.Automation.PSCredential ("{username}", $securePass)
        """
