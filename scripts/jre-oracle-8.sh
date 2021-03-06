#!/usr/bin/env bash
# Filename:     jre-oracle-8.sh installer.sh
# Purpose:      install oracle java jre version 8
#------------------------------------------------------------------------------

INSTALL="apt-get install -y --force-yes --no-install-recommends"
UPDATE="apt-get update"
PACKAGES="oracle-java8-installer oracle-java8-set-default"

echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main"> /etc/apt/sources.list.d/webupd8team-java.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886

echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

eval "$UPDATE"

# Workaround because of latest oracle java update
apt-get install -y oracle-java8-installer || true \
&& cd /var/lib/dpkg/info \
&& sed -i 's|JAVA_VERSION=8u171|JAVA_VERSION=8u181|' oracle-java8-installer.* \
&& sed -i 's|PARTNER_URL=http://download.oracle.com/otn-pub/java/jdk/8u171-b11/512cd62ec5174c3487ac17c61aaa89e8/|PARTNER_URL=http://download.oracle.com/otn-pub/java/jdk/8u181-b13/96a7b8442fe848ef90c96a2fad6ed6d1/|' oracle-java8-installer.* \
&& sed -i 's|SHA256SUM_TGZ=".*"|SHA256SUM_TGZ="d78a023abffb7ce4aade43e6db64bbad5984e7c82c54c332da445c9a79c1a904"|' oracle-java8-installer.* \
&& sed -i 's|J_DIR=jdk1.8.0_171|J_DIR=jdk1.8.0_181|' oracle-java8-installer.* \


eval "$INSTALL $PACKAGES"

exit 0
