import pytest

@pytest.mark.parametrize("name,version", [
    ("mysql-server", "5.5"),
    ("python", "2.7"),
])
def test_basic_packages_installed(Package, name, version):
    assert Package(name).is_installed
    assert Package(name).version.startswith(version)


@pytest.mark.parametrize("user", [
    ("root"),
    ("openthinclient"),
])

def test_user_in_passwd_file(File, user):
    passwd = File("/etc/passwd")
    assert passwd.contains(user)


@pytest.mark.parametrize("service_name", [
    ("openthinclient-manager"),
    ("lightdm"),
    ("mysql"),
])

def test_service_running(Service, service_name):
    service = Service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,host,port", [
    ("tcp", "127.0.0.1", "3306"),
    ("tcp", "0.0.0.0","22"),
])

def test_socket_listening(Socket, proto, host, port):
    socketoptions = "{0}://{1}:{2}".format(proto, host, port)
    socket = Socket(socketoptions)
    assert socket.is_listening


def test_passwd_file(File):
    passwd = File("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644

def test_openthinclient_manager_file(File):
    managerbin = File("/opt/openthinclient/bin/openthinclient-manager")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-manager"),
    ("/usr/local/bin/openthinclient-vmversion"),
])

def test_otc_usr_local_bin_files(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/sbin/openthinclient-changepassword"),
    ("/usr/local/sbin/openthinclient-cleaner"),
    ("/usr/local/sbin/openthinclient-edit-sources-lst-lite"),
    ("/usr/local/sbin/openthinclient-ldapbackup"),
    ("/usr/local/sbin/openthinclient-restart"),
    ("/usr/local/sbin/zerofree.sh"),
])

def test_otc_usr_local_sbin_files(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True

def test_crond_ldap_backup_file(File):
    managerbin = File("/etc/cron.d/openthinclient_ldap_backup")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists == True


@pytest.mark.parametrize("filename,content", [
    ("/etc/sudoers.d/90-openthinclient-appliance", "openthinclient ALL=(ALL) NOPASSWD:ALL"),
])

def test_sudoers_file(File, filename, content, Command, Sudo):
    file = File(filename)
    with Sudo():
        Command.check_output("whoami")
        assert file.contains(content)
        assert file.user == "root"
        assert file.group == "root"
        assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/etc/X11/Xsession.d/21-lightdm-locale-fix"),
])

def test_otc_gui_lightdm_locale_fix(File, filename):
    file = File(filename)
    assert file.user == "root"
    assert file.group == "root"
    assert file.exists == True
    # assert file.mode == 0o744 # FIXME - check if this needs to executable


@pytest.mark.parametrize("filename", [
    ("/etc/lightdm/lightdm.conf"),
])

def test_lightdm_config_file(File, filename):
    file = File(filename)
    #assert file.user == "root"
    #assert file.group == "root"
    assert file.exists == True



@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm.conf", "greeter-setup-script=/usr/local/bin/openthinclient-default-user-fix" ),
    ("/etc/lightdm/lightdm.conf", "allow-guest=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-hide-users=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-show-manual-login=true"),
])

def test_lightdm_config_content(File, filename, content):
    file = File(filename)
    assert file.contains(content)
    #assert file.group == "root"
    assert file.exists == True


@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm-gtk-greeter.conf",
        "background=/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg" ),
    ("/etc/lightdm/lightdm-gtk-greeter.conf", "show-clock=true"),
])

def test_lightdm_config_content(File, filename, content):
    file = File(filename)
    assert file.contains(content)
    #assert file.group == "root"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-default-user-fix"),
    ("/usr/local/bin/openthinclient-keyboard-layout-fix"),
    ("/home/openthinclient/.config/autostart/keyboard-layout-fix.desktop"),
])

def test_otc_gui_fixes_via_script(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/home/openthinclient/Desktop/Buy hardware.desktop"),
    ("/home/openthinclient/Desktop/change password.desktop"),
    ("/home/openthinclient/Desktop/Edit openthinclient package sources.desktop"),
    ("/home/openthinclient/Desktop/Feature Bid.desktop"),
    ("/home/openthinclient/Desktop/livesupport.levigo.de.desktop"),
    ("/home/openthinclient/Desktop/mate-network-properties.desktop"),
    ("/home/openthinclient/Desktop/mate-time.desktop"),
    ("/home/openthinclient/Desktop/openthinclient Manager.desktop"),
    ("/home/openthinclient/Desktop/openthinclient Package Manager.desktop"),
    ("/home/openthinclient/Desktop/openthinclient service restart.desktop"),
    ("/home/openthinclient/Desktop/Oracle-Java-Licence"),
    ("/home/openthinclient/Desktop/professional support & hardware.desktop"),
    ("/home/openthinclient/Desktop/README.desktop"),
    #("/home/openthinclient/Desktop/teamviewer-teamviewer9.desktop"),
    ("/home/openthinclient/Desktop/Version-Information.desktop"),
    ("/home/openthinclient/Desktop/VNC Viewer.desktop"),
])

def test_otc_desktop_icons(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg"),
    ("/usr/local/share/openthinclient/backgrounds/desktopB_1920x1200.png"),
    ("/usr/local/share/openthinclient/backgrounds/OTC_VM_1280x1024.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_advisor.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_ceres_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_consus_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient-features.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_manager.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_minerva_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_pales_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_professional_support.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_readme.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_service_restart.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_shop.png"),
])

def test_otc_background_and_icons(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True

@pytest.mark.parametrize("name,version", [
    ("mate-desktop-environment-core", "1.8"),
    ("lightdm", "1.10"),
])

def test_gui_packages_installed(Package, name, version):
    assert Package(name).is_installed
    assert Package(name).version.startswith(version)


@pytest.mark.parametrize("name", [
    ("rpcbind"),
])
def test_package_cleanup(Package, name):
    assert Package(name).is_installed == False