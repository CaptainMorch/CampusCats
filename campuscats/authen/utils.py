import ipaddress


def parse_trusted_networks_setting(*entries):
    """parse the setting to a list of IPv4Network"""
    domains = []
    for entry in entries:
        if isinstance(entry, str):
            # should represent network or ip address.
            # sigle ip address will be convert to a sigle-address network
            try:
                network = ipaddress.IPv4Network(entry)
            except ipaddress.AddressValueError:
                raise ValueError(f'"{entry}" should be a string '
                    'representing an IPv4 Address or IPv4 Network.')
            else:
                domains.append(network)
                continue

        # must be a 2-tuple representing network
        try:
            ip_start, ip_end = entry
        except ValueError:
            raise ValueError(f'"{entry}" should be a 2-tuple')

        try:
            ip_start = ipaddress.IPv4Address(ip_start)
            ip_end = ipaddress.IPv4Address(ip_end)
        except ipaddress.AddressValueError:
            raise ValueError(f'{entry} contains invalid IPv4 address')

        # the default exception massage is clear enough
        networks_iter = ipaddress.summarize_address_range(
            ip_start, ip_end)

        for network in networks_iter:
            domains.append(network)
    return domains