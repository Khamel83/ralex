# Security Considerations for Ralex

## Network Security

### API Endpoints
- **RalexBridge API** (port 8000): Currently no authentication required
- **OpenWebUI** (port 3000): Basic session management
- **Recommendation**: Deploy behind reverse proxy with authentication for production

### Network Configuration
- Default: Binds to `0.0.0.0` (all interfaces) for RPi deployment
- Mobile access: Requires devices on same network
- Remote access: Use VPN (Tailscale recommended) vs port forwarding

## API Key Management

### OpenRouter API Key
- **Critical**: Never commit to version control
- **Storage**: Environment variable only (`.env` file)
- **Rotation**: Change regularly if compromised
- **Monitoring**: Track usage in OpenRouter dashboard

### Mobile App Configuration
- **API Key field**: Any value accepted (no validation currently)
- **Base URL**: Transmitted in plain text over local network
- **Recommendation**: Use HTTPS in production deployment

## Rate Limiting

### Current Implementation
- **None**: No built-in rate limiting
- **OpenRouter**: Subject to upstream rate limits
- **Mobile clients**: Can overwhelm local API

### Recommendations
- Implement basic rate limiting (10 requests/minute per IP)
- Monitor cost usage in `.ralex/cost_log.txt`
- Set daily/weekly budgets in configuration

## Data Handling

### Conversation Data
- **Storage**: Not persisted by default
- **OpenWebUI**: Stores chat history in local database
- **Mobile apps**: Data handling varies by app

### File Access
- **Scope**: Full filesystem access via OpenCode integration
- **Risk**: Mobile queries could trigger file operations
- **Mitigation**: Validate commands before execution

## Production Deployment

### Minimum Security Measures
1. **Reverse proxy**: nginx/caddy with HTTPS
2. **Authentication**: Basic auth or API keys
3. **Network isolation**: Internal network only
4. **Monitoring**: Log all API requests
5. **Backups**: Configuration and chat data

### Environment Hardening
```bash
# Set restrictive permissions
chmod 600 .env
chmod 700 .ralex/

# Create dedicated user
sudo useradd -m -s /bin/bash ralex
sudo -u ralex python start_ralex_v4.py
```

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 8000  # RalexBridge API
sudo ufw allow 3000  # OpenWebUI (optional)
sudo ufw enable
```

## Mobile App Security

### OpenCat
- **Data transmission**: Check app privacy policy
- **Local storage**: Conversations may be cached locally
- **API key**: Transmitted with each request

### General Mobile Security
- **Network**: Use trusted WiFi networks only
- **App permissions**: Review what each app can access
- **Updates**: Keep mobile apps updated

## Monitoring and Auditing

### Log Files
- **Cost tracking**: `.ralex/cost_log.txt`
- **System logs**: Check via `journalctl` if using systemd
- **Application logs**: stdout/stderr from startup script

### Key Metrics to Monitor
- API request frequency and patterns
- Cost accumulation and budget adherence
- Error rates and types
- Network connection attempts

### Alerting Recommendations
- Daily cost threshold exceeded
- Unusual request patterns
- Authentication failures (when implemented)
- System resource exhaustion

## Incident Response

### Compromised API Key
1. Immediately revoke in OpenRouter dashboard
2. Generate new API key
3. Update `.env` file
4. Restart Ralex services
5. Monitor for unauthorized usage

### Suspicious Activity
1. Check cost logs for unusual patterns
2. Review system logs for unauthorized access
3. Change any authentication credentials
4. Consider network isolation until investigation complete

---

**Note**: This security model prioritizes ease of use for development/personal use. Production deployments require additional hardening measures based on threat model and compliance requirements.