# authen
Provides an user model and two permissions that can be easily set to different predefined strategies. One controls how location info of cats are restricted from viewing, and the other controls how non-sensitive 'dangerous' actions are allowed from non-member visitors.

## Settings
### Strategy
- `PERMISSION_FOR_VIEWING_LOCATIONS`: the default permission class for all location-related actions, including the 'safe' ones
- `PERMISSION_FOR_NON_SENSITIVE_ACTIONS`: the default permission class for these non-sensitive 'dangerous' actions:
    - `POST /api/cats/report-new/`
    - `POST /api/cats/<int: pk>/report/`
    - `POST /api/media/uploads/img/`
    - `POST /api/suggetions/`

both settings accept a string path to a permission class, either predefined as follow or not. both defaults to `authen.permissions.TrustByEmailNetworkGroup`

**permissions predefined in `authen.permissions`**:
- `AllowAny`: no limitations, same rule as public api
- `MembersOnly`: members-only, same rule as admin site
- `TrustByEmail`: allow users with activated email of trusted domains, or members
- `TrustByNetwork`: allow requests from ip in trusted networks, or members
- `TrustByEmailNetwork`: allow members and users with trusted verified email, or from trusted network
- `TrustByEmailNetworkGroup`(default): allow members and users with trusted verified email, or from trusted network or group

### Values
`TRUSTED_EMAIL_DOMAINS`: a list of email suffixes to be regarded as trusted. Add `''` to regard all *verified* email as trusted. Eg. `['@tongji.edu.cn']`

`TRUSTED_USER_GROUP`: a string, name of the trusted user group. default to `trusted`

`TRUSTED_NETWORKS`: a function call to `utils.trusting.parser.parse_trusted_networks_setting`. The function accepts arbitrary number of following arguments:
- string representing an ipv4-address, e.g. `0.0.0.1`
- string representing an ipv4-network, e.g. `0.0.0.0/24`
- two-tuple consisting two strings of ipv4-address, representing the start and the end of an ipv4-network, e.g. `('0.0.0.0', '0.0.0.255')`