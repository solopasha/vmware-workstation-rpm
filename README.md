# vmware-workstation RPMs

An initial rough attempt to package vmware-workstation for fedora...

```bash
sudo dnf -y install fedora-packager
git clone https://github.com/solopasha/vmware-workstation-rpm.git
cd vmware-workstation-rpm/vmware-workstation
spectool -g ./vmware-workstation.spec
fedpkg --release f38 mockbuild
```

Install the resulting vmware-workstation rpm package from vmware-workstation/results_vmware-workstation/... along with the akmod-vmware-workstation package from the Releases page.
