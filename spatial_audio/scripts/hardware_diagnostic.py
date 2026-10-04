import os
import subprocess
import platform

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""

def check_file(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except:
            return f"Error reading {path}"
    return "Not found"

def check_gpio_mode(pin):
    # Try pinctrl (raspi-gpio replacement for pi 5)
    # or raspi-gpio
    output = run_cmd(f"pinctrl get {pin} 2>/dev/null || raspi-gpio get {pin} 2>/dev/null")
    if output:
        return output
    return f"Unable to read GPIO {pin}"

def main():
    print("================================")
    print("    HARDWARE DIAGNOSTIC TOOL    ")
    print("================================")
    
    print("\nSYSTEM INFO")
    print("-----------")
    print(f"OS/Kernel: {platform.system()} {platform.release()} ({platform.machine()})")
    
    model = check_file("/sys/firmware/devicetree/base/model")
    print(f"Model: {model}")
    
    print("\nI2S HARDWARE")
    print("============")
    
    gpios = {
        18: ("BCLK", "GPIO18"),
        19: ("WS", "GPIO19"),
        20: ("SDI0 (MIC1)", "GPIO20"),
        22: ("SDI1 (MIC2)", "GPIO22"),
        24: ("SDI2 (MIC3)", "GPIO24"),
        26: ("SDI3 (MIC4)", "GPIO26"),
    }
    
    i2s_pass = True
    for pin, (func, name) in gpios.items():
        state = check_gpio_mode(pin)
        # simplistic check
        status = "PASS" if "I2S" in state or "ALT" in state else "FAIL/UNKNOWN"
        print(f"{name:<6} {func:<12} {status:<15} (Raw: {state})")
        if status != "PASS":
            i2s_pass = False

    print("\nALSA CAPTURE")
    print("============")
    
    cards = check_file("/proc/asound/cards")
    pcm = check_file("/proc/asound/pcm")
    
    print(f"Cards:\n{cards}")
    print(f"\nPCM Devices:\n{pcm}")
    
    arecord_l = run_cmd("arecord -l")
    print(f"\nCapture Devices (arecord -l):\n{arecord_l}")
    
    device_detected = "snd" in cards.lower() or "i2s" in arecord_l.lower() or "snd_rp1" in arecord_l.lower()
    print(f"\nDevice detected: {'YES' if device_detected else 'NO'}")
    
    alsa_pass = device_detected
    
    print("\nDEVICE TREE & MODULES")
    print("---------------------")
    lsmod = run_cmd("lsmod | grep snd")
    print(f"Loaded sound modules:\n{lsmod}")
    
    config_txt = ""
    if os.path.exists("/boot/firmware/config.txt"):
        config_txt = run_cmd("grep -i -E 'dtparam=i2s|dtoverlay=.*i2s|snd|rp1' /boot/firmware/config.txt")
    elif os.path.exists("/boot/config.txt"):
        config_txt = run_cmd("grep -i -E 'dtparam=i2s|dtoverlay=.*i2s|snd|rp1' /boot/config.txt")
    
    print(f"\nconfig.txt I2S/Audio config:\n{config_txt}")
    
    print("\nOVERALL:")
    if i2s_pass and alsa_pass:
        print("PASS")
    elif i2s_pass or alsa_pass:
        print("PARTIAL")
    else:
        print("FAIL")

if __name__ == "__main__":
    main()
