def get_client_ip(request):
    """The visitor's IP, as seen by kamal-proxy.

    kamal-proxy is the only proxy in front of the app, and it adds the address it
    received the connection from as the last X-Forwarded-For entry. Anything
    earlier in that header came from the client and can be forged, so only the
    last entry is trusted. Without the header (local dev), use REMOTE_ADDR.
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    hops = [hop.strip() for hop in forwarded.split(",") if hop.strip()]
    return hops[-1] if hops else request.META.get("REMOTE_ADDR")
