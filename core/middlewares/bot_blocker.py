import logging
from django.http import HttpResponseForbidden

# Configure logging
logging.basicConfig(
    filename='bot_scan.log',  # Log file name
    level=logging.INFO,       # Log level
    format='%(asctime)s - %(message)s'  # Log format
)

# Extended list of known security scanners, forensic tools, and malicious bots
BLOCKED_USER_AGENTS = [
    "Googlebot", "bingbot", "Amazonbot", "PhishTank", "CloudflareScanner", 
    "CiscoUmbrella", "VirusTotal", "SecurityBot", "Zgrab", "Censys", "Shodan", 
    "Nmap", "Masscan", "OpenVAS", "Nikto", "Wget", "cURL", "sqlmap", 
    "Mozilla/5.0 zgrab", "Mozilla/5.0 masscan", "Metasploit", "BurpSuite", 
    "OWASP", "Maltego", "CheckPhish", "Netcraft", "HybridAnalysis"
]

class BlockScannersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        for bot in BLOCKED_USER_AGENTS:
            if bot in user_agent:
                # Log the blocked bot
                logging.info(f"Blocked bot: {bot} - User-Agent: {user_agent}")
                return HttpResponseForbidden("403 Forbidden")
        return self.get_response(request)
