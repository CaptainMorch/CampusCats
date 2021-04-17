# Trusting
Simple authenticating layer, especially for filtering non-sensitive
requests that alter server states.

## Settings
### Strategy
`TRUSTING_FUNCTION`: string path to a function which accepts a `Request` instance and returns a bool indicating whether it's regarded as trusted.

**trusting functions predifined in `utils.trusting`**:
- `trust_all`: same rule as public api, i.e. no limitations
- `trust_only_staff`: same rule as admin site
- `trust_by_network_email`(default): Trust staffs and users with trusted verified email, or from trusted network
- `trust_by_network_email_group`: Trust staffs and users with trusted verified email, or from trusted network or group

### Values
`TRUSTED_EMAIL_DOMAINS`: a list of email suffixes to be regarded as trusted. Add `''` to regard all *verified* email as trusted. Eg. `['@tongji.edu.cn']`

`TRUSTED_USER_GROUP`: a string, name of the trusted user group. Won't work with default trusting strategy setting

`TRUSTED_NETWORKS`: a function call to `utils.trusting.parser.parse_trusted_networks_setting`. The function accepts arbitrary number of following arguments:
- string representing an ipv4-address, e.g. `0.0.0.1`
- string representing an ipv4-network, e.g. `0.0.0.0/24`
- two-tuple consisting two strings of ipv4-address, representing the start and the end of an ipv4-network, e.g. `('0.0.0.0', '0.0.0.255')`

## Usage
### Middleware
Add `utils.trusting.TrustingMiddleware` to `MIDDLEWARES` setting, below `django.contrib.auth.middleware.AuthenticationMiddleware`, than you can access the `is_trusted` property of `request` object anywhere

### decorator
`utils.trusting.trusted_required`: decorator for views that only allow request from trusted source. Return a `HttpResponseForbidden` instance on fail. `utils.trusting.TrustingMiddleware` required

### rest_framwork permission class
(all `utils.trusting.TrustingMiddleware` required)

`utils.trusting.IsTrusted`: allows access only from trusted source

`utils.trusting.IsTrustedOrReadOnly`: only allows 'safe' request from untrusted source