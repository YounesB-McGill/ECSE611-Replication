# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import 'stages.pp'
# both of these should be symlnks to the appropriate organization
import 'config.pp'
import 'nodes.pp'

# Default to 0:0, 0644 on POSIX, and root, 0644 on Windows
case $::operatingsystem {
    Windows: {
        File {
            owner              => root,
            backup             => false,
            mode               => filemode(0644),
            source_permissions => ignore,
        }
    }
    default: {
        File {
            owner  => 0,
            group  => 0,
            mode   => filemode(0644),
            backup => false,
        }
    }
}

Concat {
    backup => false
}

Concat::Fragment {
    backup => false
}

# purge unknown users from the system's user database.  This doesn't work on Windows
# due to https://projects.puppetlabs.com/issues/22048
# TODO-WIN: figre out how to not purge system users on windows (solve the puppetlabs bug)
if ($::operatingsystem != 'windows') {
    resources {
        'user':
            purge              => true,
            # default for this is 500, but puppet assumes uids <= unless_system_user are system
            # users, meaning that 500 is considered a system user.  This is not what we want!
            # see https://tickets.puppetlabs.com/browse/PUP-3160
            unless_system_user => 499;
    }
}

# The PuppetLabs firewall module is only supported on Linux
case $::operatingsystem {
    CentOS,Ubuntu: {
        # Let's make sure iptables and iptables-ipv6 is installed on centos and ubuntu
        # https://tickets.puppetlabs.com/browse/PUP-1963
        # https://tickets.puppetlabs.com/browse/PUP-5874
        if ($::operatingsystem == 'CentOS') or ($::operatingsystem == 'Ubuntu') {
            include packages::iptables
        }

        # Purging all unmanaged firewall rules was removed in favor of explicitly
        # purging just the 'Big 3' chains since these are what really matter and
        # what we are trying managing anyway.  This also allows for Docker to manage
        # its own rules dynamically as we can ignore them through the use of regex.
        # See bug 1429240

        $chain_purge = true
        $chain_purge_ignore = [
            '-o docker0',
            '-i docker0',
            'DOCKER',
            'DOCKER-USER',
            'DOCKER-ISOLATION',
            'br-',
        ]

        # IPv4 Chains
        firewallchain { 'INPUT:filter:IPv4':
            ensure => 'present',
            purge  => $chain_purge,
            ignore => $chain_purge_ignore,
        }
        firewallchain { 'OUTPUT:filter:IPv4':
            ensure => 'present',
            purge  => $chain_purge,
            ignore => $chain_purge_ignore,
        }
        firewallchain { 'FORWARD:filter:IPv4':
            ensure => 'present',
            purge  => $chain_purge,
            ignore => $chain_purge_ignore,
        }

        # IPv6 chains
        firewallchain { 'INPUT:filter:IPv6':
            ensure => 'present',
            purge  => $chain_purge,
            ignore => $chain_purge_ignore,
        }
        firewallchain { 'OUTPUT:filter:IPv6':
            ensure => 'present',
            purge  => $chain_purge,
            ignore => $chain_purge_ignore,
        }
        firewallchain { 'FORWARD:filter:IPv6':
            ensure => 'present',
            purge  => $chain_purge,
            ignore => $chain_purge_ignore,
        }

        # put the default rules before/after any custom rules
        Firewall {
            require => Class['fw::pre'],
            before  => Class['fw::post'],
        }
    }
    default: {
        # silently not supported
    }
}

if versioncmp($::puppetversion,'3.6.1') >= 0 {

  $allow_virtual_packages = hiera('allow_virtual_packages',false)

  Package {
    allow_virtual => $allow_virtual_packages,
  }
}
ThisIsPascalCase
thisIsCamelCase
thisIsCamelCaseWithStemmableWords