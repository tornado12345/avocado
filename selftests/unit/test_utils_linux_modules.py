import io
import unittest.mock

from .. import recent_mock
from avocado.utils import linux_modules


class TestLsmod(unittest.TestCase):

    LSMOD_OUT = """\
Module                  Size  Used by
ccm                    17773  2
ip6t_rpfilter          12546  1
ip6t_REJECT            12939  2
xt_conntrack           12760  9
ebtable_nat            12807  0
ebtable_broute         12731  0
bridge                110862  1 ebtable_broute
stp                    12868  1 bridge
llc                    13941  2 stp,bridge
ebtable_filter         12827  0
ebtables               30758  3 ebtable_broute,ebtable_nat,ebtable_filter
ip6table_nat           13015  1
nf_conntrack_ipv6      18738  6
nf_defrag_ipv6         34712  1 nf_conntrack_ipv6
nf_nat_ipv6            13213  1 ip6table_nat
ip6table_mangle        12700  1
ip6table_security      12710  1
ip6table_raw           12683  1
ip6table_filter        12815  1
"""

    PROC_MODULES_OUT = b"""snd_usb_audio 225280 0 - Live 0x0000000000000000
snd_usbmidi_lib 32768 1 snd_usb_audio, Live 0x0000000000000000
snd_rawmidi 36864 1 snd_usbmidi_lib, Live 0x0000000000000000
hid_plantronics 16384 0 - Live 0x0000000000000000
ccm 20480 0 - Live 0x0000000000000000
usblp 24576 0 - Live 0x0000000000000000
rfcomm 86016 4 - Live 0x0000000000000000
xt_CHECKSUM 16384 1 - Live 0x0000000000000000
ipt_MASQUERADE 16384 3 - Live 0x0000000000000000
nf_nat_masquerade_ipv4 16384 1 ipt_MASQUERADE, Live 0x0000000000000000
tun 49152 3 - Live 0x0000000000000000
ip6t_rpfilter 16384 1 - Live 0x0000000000000000
ip6t_REJECT 16384 2 - Live 0x0000000000000000
nf_reject_ipv6 16384 1 ip6t_REJECT, Live 0x0000000000000000
xt_conntrack 16384 14 - Live 0x0000000000000000
devlink 61440 0 - Live 0x0000000000000000
ip_set 45056 0 - Live 0x0000000000000000
hidp 28672 0 - Live 0x0000000000000000
nfnetlink 16384 1 ip_set, Live 0x0000000000000000
ebtable_nat 16384 1 - Live 0x0000000000000000
ebtable_broute 16384 1 - Live 0x0000000000000000
bridge 188416 1 ebtable_broute, Live 0x0000000000000000
stp 16384 1 bridge, Live 0x0000000000000000
llc 16384 2 bridge,stp, Live 0x0000000000000000
ip6table_nat 16384 1 - Live 0x0000000000000000
nf_conntrack_ipv6 16384 8 - Live 0x0000000000000000
nf_defrag_ipv6 20480 1 nf_conntrack_ipv6, Live 0x0000000000000000
nf_nat_ipv6 16384 1 ip6table_nat, Live 0x0000000000000000
ip6table_mangle 16384 1 - Live 0x0000000000000000
ip6table_raw 16384 1 - Live 0x0000000000000000
ip6table_security 16384 1 - Live 0x0000000000000000
iptable_nat 16384 1 - Live 0x0000000000000000
nf_conntrack_ipv4 16384 11 - Live 0x0000000000000000
nf_defrag_ipv4 16384 1 nf_conntrack_ipv4, Live 0x0000000000000000
nf_nat_ipv4 16384 1 iptable_nat, Live 0x0000000000000000
nf_nat 36864 3 nf_nat_masquerade_ipv4,nf_nat_ipv6,nf_nat_ipv4, Live 0x0000000000000000
nf_conntrack 147456 8 ipt_MASQUERADE,nf_nat_masquerade_ipv4,xt_conntrack,nf_conntrack_ipv6,nf_nat_ipv6,nf_conntrack_ipv4,nf_nat_ipv4,nf_nat, Live 0x0000000000000000
iptable_mangle 16384 1 - Live 0x0000000000000000
iptable_raw 16384 1 - Live 0x0000000000000000
iptable_security 16384 1 - Live 0x0000000000000000
ebtable_filter 16384 1 - Live 0x0000000000000000
ebtables 36864 3 ebtable_nat,ebtable_broute,ebtable_filter, Live 0x0000000000000000
ip6table_filter 16384 1 - Live 0x0000000000000000
ip6_tables 32768 7 ip6table_nat,ip6table_mangle,ip6table_raw,ip6table_security,ip6table_filter, Live 0x0000000000000000
cmac 16384 1 - Live 0x0000000000000000
bnep 24576 2 - Live 0x0000000000000000
sunrpc 430080 1 - Live 0x0000000000000000
dm_crypt 40960 1 - Live 0x0000000000000000
dm_thin_pool 77824 1 - Live 0x0000000000000000
dm_persistent_data 90112 1 dm_thin_pool, Live 0x0000000000000000
dm_bio_prison 20480 1 dm_thin_pool, Live 0x0000000000000000
uvcvideo 114688 0 - Live 0x0000000000000000
videobuf2_vmalloc 16384 1 uvcvideo, Live 0x0000000000000000
videobuf2_memops 16384 1 videobuf2_vmalloc, Live 0x0000000000000000
videobuf2_v4l2 28672 1 uvcvideo, Live 0x0000000000000000
videobuf2_common 53248 2 uvcvideo,videobuf2_v4l2, Live 0x0000000000000000
videodev 208896 3 uvcvideo,videobuf2_v4l2,videobuf2_common, Live 0x0000000000000000
btusb 53248 0 - Live 0x0000000000000000
btrtl 16384 1 btusb, Live 0x0000000000000000
btbcm 16384 1 btusb, Live 0x0000000000000000
media 45056 2 uvcvideo,videodev, Live 0x0000000000000000
btintel 24576 1 btusb, Live 0x0000000000000000
bluetooth 598016 32 rfcomm,hidp,bnep,btusb,btrtl,btbcm,btintel, Live 0x0000000000000000
ecdh_generic 24576 2 bluetooth, Live 0x0000000000000000
rmi_smbus 16384 0 - Live 0x0000000000000000
rmi_core 81920 1 rmi_smbus, Live 0x0000000000000000
arc4 16384 2 - Live 0x0000000000000000
intel_rapl 24576 0 - Live 0x0000000000000000
x86_pkg_temp_thermal 16384 0 - Live 0x0000000000000000
intel_powerclamp 16384 0 - Live 0x0000000000000000
coretemp 16384 0 - Live 0x0000000000000000
kvm_intel 237568 0 - Live 0x0000000000000000
iwlmvm 425984 0 - Live 0x0000000000000000
kvm 724992 1 kvm_intel, Live 0x0000000000000000
mac80211 909312 1 iwlmvm, Live 0x0000000000000000
snd_hda_codec_hdmi 57344 1 - Live 0x0000000000000000
snd_hda_codec_realtek 110592 1 - Live 0x0000000000000000
iTCO_wdt 16384 0 - Live 0x0000000000000000
irqbypass 16384 1 kvm, Live 0x0000000000000000
mei_wdt 16384 0 - Live 0x0000000000000000
iTCO_vendor_support 16384 1 iTCO_wdt, Live 0x0000000000000000
snd_hda_codec_generic 86016 1 snd_hda_codec_realtek, Live 0x0000000000000000
crct10dif_pclmul 16384 0 - Live 0x0000000000000000
gpio_ich 16384 0 - Live 0x0000000000000000
crc32_pclmul 16384 0 - Live 0x0000000000000000
snd_hda_intel 45056 7 - Live 0x0000000000000000
ghash_clmulni_intel 16384 0 - Live 0x0000000000000000
snd_hda_codec 151552 4 snd_hda_codec_hdmi,snd_hda_codec_realtek,snd_hda_codec_generic,snd_hda_intel, Live 0x0000000000000000
intel_cstate 16384 0 - Live 0x0000000000000000
snd_hda_core 94208 5 snd_hda_codec_hdmi,snd_hda_codec_realtek,snd_hda_codec_generic,snd_hda_intel,snd_hda_codec, Live 0x0000000000000000
intel_uncore 131072 0 - Live 0x0000000000000000
iwlwifi 262144 1 iwlmvm, Live 0x0000000000000000
snd_hwdep 16384 2 snd_usb_audio,snd_hda_codec, Live 0x0000000000000000
intel_rapl_perf 16384 0 - Live 0x0000000000000000
snd_seq 81920 0 - Live 0x0000000000000000
snd_seq_device 16384 2 snd_rawmidi,snd_seq, Live 0x0000000000000000
cfg80211 770048 3 iwlmvm,mac80211,iwlwifi, Live 0x0000000000000000
snd_pcm 118784 5 snd_usb_audio,snd_hda_codec_hdmi,snd_hda_intel,snd_hda_codec,snd_hda_core, Live 0x0000000000000000
thinkpad_acpi 106496 1 - Live 0x0000000000000000
joydev 24576 0 - Live 0x0000000000000000
wmi_bmof 16384 0 - Live 0x0000000000000000
snd_timer 36864 2 snd_seq,snd_pcm, Live 0x0000000000000000
rfkill 28672 8 bluetooth,cfg80211,thinkpad_acpi, Live 0x0000000000000000
snd 94208 28 snd_usb_audio,snd_usbmidi_lib,snd_rawmidi,snd_hda_codec_hdmi,snd_hda_codec_realtek,snd_hda_codec_generic,snd_hda_intel,snd_hda_codec,snd_hwdep,snd_seq,snd_seq_device,snd_pcm,thinkpad_acpi,snd_timer, Live 0x0000000000000000
mei_me 45056 1 - Live 0x0000000000000000
soundcore 16384 1 snd, Live 0x0000000000000000
mei 110592 3 mei_wdt,mei_me, Live 0x0000000000000000
i2c_i801 28672 0 - Live 0x0000000000000000
ie31200_edac 16384 0 - Live 0x0000000000000000
lpc_ich 28672 0 - Live 0x0000000000000000
pcc_cpufreq 16384 0 - Live 0x0000000000000000
shpchp 40960 0 - Live 0x0000000000000000
xfs 1581056 3 - Live 0x0000000000000000
libcrc32c 16384 4 nf_nat,nf_conntrack,dm_persistent_data,xfs, Live 0x0000000000000000
i915 2052096 18 - Live 0x0000000000000000
i2c_algo_bit 16384 1 i915, Live 0x0000000000000000
drm_kms_helper 196608 1 i915, Live 0x0000000000000000
drm 458752 10 i915,drm_kms_helper, Live 0x0000000000000000
sdhci_pci 40960 0 - Live 0x0000000000000000
cqhci 28672 1 sdhci_pci, Live 0x0000000000000000
sdhci 57344 1 sdhci_pci, Live 0x0000000000000000
crc32c_intel 24576 2 - Live 0x0000000000000000
e1000e 282624 0 - Live 0x0000000000000000
serio_raw 16384 0 - Live 0x0000000000000000
mmc_core 172032 3 sdhci_pci,cqhci,sdhci, Live 0x0000000000000000
wmi 32768 1 wmi_bmof, Live 0x0000000000000000
video 45056 2 thinkpad_acpi,i915, Live 0x0000000000000000
"""

    @staticmethod
    def _get_file_mock(content):
        file_mock = unittest.mock.Mock()
        file_mock.__enter__ = unittest.mock.Mock(return_value=io.BytesIO(content))
        file_mock.__exit__ = unittest.mock.Mock()
        return file_mock

    def test_parse_lsmod(self):
        lsmod_info = linux_modules.parse_lsmod_for_module(
            self.LSMOD_OUT, "ebtables")
        self.assertEqual(lsmod_info, {'name': "ebtables",
                                      'size': 30758,
                                      'used': 3,
                                      'submodules': ['ebtable_broute',
                                                     'ebtable_nat',
                                                     'ebtable_filter']})

    def test_parse_lsmod_is_empty(self):
        lsmod_info = linux_modules.parse_lsmod_for_module("", "ebtables")
        self.assertEqual(lsmod_info, {})

    def test_parse_lsmod_no_submodules(self):
        lsmod_info = linux_modules.parse_lsmod_for_module(self.LSMOD_OUT, "ccm")
        self.assertEqual(lsmod_info, {'name': "ccm",
                                      'size': 17773,
                                      'used': 2,
                                      'submodules': []})

    def test_parse_lsmod_single_submodules(self):
        lsmod_info = linux_modules.parse_lsmod_for_module(
            self.LSMOD_OUT, "bridge")
        self.assertEqual(lsmod_info, {'name': "bridge",
                                      'size': 110862,
                                      'used': 1,
                                      'submodules': ['ebtable_broute']})

    @unittest.skipUnless(recent_mock(),
                         "mock library version cannot (easily) patch open()")
    def test_is_module_loaded(self):
        with unittest.mock.patch('avocado.utils.linux_modules.open',
                                 return_value=self._get_file_mock(self.PROC_MODULES_OUT)):
            self.assertTrue(linux_modules.module_is_loaded("rfcomm"))
            self.assertFalse(linux_modules.module_is_loaded("unknown_module"))


if __name__ == '__main__':
    unittest.main()
