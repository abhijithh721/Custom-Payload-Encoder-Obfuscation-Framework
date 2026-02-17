import base64
import codecs
import os

# --- ENCODING MODULES ---

def xor_cipher(data, key="KALI"):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def rot13_encode(data):
    return codecs.encode(data, 'rot_13')

def base64_encode(data):
    return base64.b64encode(data.encode()).decode()

# --- OBFUSCATION MODULES ---

def string_split(data, size=4):
    chunks = [data[i:i+size] for i in range(0, len(data), size)]
    return " + ".join([f"'{c}'" for c in chunks])

# --- MAIN ENGINE ---

def run_framework():
    input_file = "payloads/raw/raw_payload.py"
    output_dir = "payloads/output/"
    
    with open(input_file, "r") as f:
        raw_data = f.read()

    print(f"[*] Processing: {input_file}")

    # Layer 1: ROT13
    r13 = rot13_encode(raw_data)
    with open(f"{output_dir}payload_rot13.txt", "w") as f: f.write(r13)

    # Layer 2: Base64
    b64 = base64_encode(raw_data)
    with open(f"{output_dir}payload_base64.txt", "w") as f: f.write(b64)

    # Layer 3: XOR + String Splitting (Multi-layered)
    xor_data = xor_cipher(raw_data)
    final_obfuscated = string_split(xor_data)
    with open(f"{output_dir}payload_obfuscated.py", "w") as f:
        f.write(f"# Multi-layered Obfuscation\ndata = {final_obfuscated}")

    print("[+] All layers generated in payloads/output/")

def generate_report():
    test_files = [
        ("Raw", "payloads/raw/raw_payload.py"),
        ("ROT13", "payloads/output/payload_rot13.txt"),
        ("Base64", "payloads/output/payload_base64.txt"),
        ("Multi-Layer", "payloads/output/payload_obfuscated.py")
    ]
    
    signature = "import"
    
    print("\n--- EVASION TEST REPORT ---")
    with open("evasion_report.txt", "w") as report:
        report.write("Method | Signature Found | Result\n")
        report.write("-" * 35 + "\n")
        
        for name, path in test_files:
            if os.path.exists(path):
                with open(path, "r") as f:
                    content = f.read()  
                    found = signature in content
                    status = "DETECTED" if found else "BYPASSED"
                    
                    result_line = f"{name.ljust(12)} | {str(found).ljust(15)} | {status}"
                    print(result_line)
                    report.write(result_line + "\n")
    
    print("\n[+] Final report saved to evasion_report.txt")

if __name__ == "__main__":
    run_framework()
    generate_report()
