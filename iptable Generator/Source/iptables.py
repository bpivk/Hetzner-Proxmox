import tkinter as tk
from tkinter import messagebox, filedialog

def generate_commands():
    # Pridobi vnesene podatke
    ip = ip_entry.get()
    port_input = port_entry.get()
    destination_ip = destination_ip_entry.get()
    interface = interface_entry.get()

    # Preverite, ali je polje prazno
    if not ip:
        messagebox.showwarning("Pozor", "Polje [Zunanji IP] ne sme biti prazno.")
        return  # Izstopi iz funkcije

    if not port_input:
        messagebox.showwarning("Pozor", "Polje [Port] ne sme biti prazno.")
        return  # Izstopi iz funkcije

    if not destination_ip:
        messagebox.showwarning("Pozor", "Polje [IP Virtualke] ne sme biti prazno.")
        return  # Izstopi iz funkcije

    if not interface:
        messagebox.showwarning("Pozor", "Polje [Mrežna kartica] ne sme biti prazno.")
        return  # Izstopi iz funkcije

    # Inicializiraj seznam ukazov
    commands = []
    console_commands = []  # Dodatno za konzolo

    # Pridobite izbrani protokol
    protocol = protocol_var.get()  # TCP ali UDP

    # Razdelite vhodne portne podatke
    port_ranges = port_input.replace(" ", "").split(',')

    all_ports = []

    # Preverite vse izbrane porte
    for port_range in port_ranges:
        if '-' in port_range:
            try:
                start_port, end_port = map(int, port_range.split('-'))
                all_ports.extend(range(start_port, end_port + 1))
            except ValueError:
                messagebox.showwarning("Pozor", f"Neveljaven obseg '{port_range}'.")
                return  # Izstopi iz funkcije
        else:
            try:
                all_ports.append(int(port_range))  # Dodajte posamezen port
            except ValueError:
                messagebox.showwarning("Pozor", f"Port '{port_range}' mora biti veljavna številka.")
                return  # Izstopi iz funkcije

    # Generiraj multiport ukaze
    port_list = ','.join(map(str, sorted(set(all_ports))))  # Uporabi set za odstranitev podvojenih portov

    # Pripravi ukaze
    post_up_command = f"post-up iptables -t nat -A PREROUTING -p {protocol} -m multiport --dports {port_list} -j DNAT --to-destination {destination_ip}"
    post_down_command = f"post-down iptables -t nat -D PREROUTING -p {protocol} -m multiport --dports {port_list} -j DNAT --to-destination {destination_ip}"

    commands.append(post_up_command)
    commands.append(post_down_command)

    # Dodajte izpise brez post-up/post-down
    console_commands.append(f"iptables -t nat -A PREROUTING -p {protocol} -m multiport --dports {port_list} -j DNAT --to-destination {destination_ip}")
    console_commands.append(f"iptables -t nat -D PREROUTING -p {protocol} -m multiport --dports {port_list} -j DNAT --to-destination {destination_ip}")

    # Izberite izhod
    if output_var.get() == "screen":
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "\n".join(commands) + "\n")
        
        # Dodajte izpis za konzolo
        console_output_text.delete(1.0, tk.END)  # Počistite prejšnji izpis
        console_output_text.insert(tk.END, "\n".join(console_commands) + "\n")  # Izpis brez post-up/post-down
        
    elif output_var.get() == "file":
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write("\n".join(commands) + "\n")
            messagebox.showinfo("Uspeh", "Ukazi shranjeni v datoteko.")

# Ustvarite glavno okno
root = tk.Tk()
root.title("Generator iptables ukazov")

# Vnosna polja
tk.Label(root, text="Zunanji IP:").grid(row=0, column=0, padx=5, pady=(2, 2), sticky='e')
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=5, pady=(2, 2), sticky='w')
ip_entry.insert(0, "95.216.13.119")  # Vnaprej izpolnjen IP

tk.Label(root, text="Port (eg. 21 ali 21-31):").grid(row=1, column=0, padx=5, pady=(2, 2), sticky='e')
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=5, pady=(2, 2), sticky='w')
port_entry.insert(0, "")  # Vnaprej izpolnjen port

tk.Label(root, text="IP Virtualke:").grid(row=2, column=0, padx=5, pady=(2, 2), sticky='e')
destination_ip_entry = tk.Entry(root)
destination_ip_entry.grid(row=2, column=1, padx=5, pady=(2, 2), sticky='w')
destination_ip_entry.insert(0, "10.10.0.*")  # Vnaprej izpolnjen ciljni IP

tk.Label(root, text="Mrežna kartica:").grid(row=3, column=0, padx=5, pady=(2, 2), sticky='e')
interface_entry = tk.Entry(root)
interface_entry.grid(row=3, column=1, padx=5, pady=(2, 2), sticky='w')
interface_entry.insert(0, "enp193s0f0np0")  # Vnaprej izpolnjen omrežni vmesnik

# Možnosti izhoda
output_var = tk.StringVar(value="screen")
radiobuttons_frame = tk.Frame(root)  # Ustvari Frame za radio gumbe
radiobuttons_frame.grid(row=4, column=0, columnspan=2, pady=(2, 2), padx=(100, 0))  # Dodano dodatno padx za okvir

# Radio gumbi za izhod
tk.Radiobutton(radiobuttons_frame, text="Pokaži na ekranu", variable=output_var, value="screen").pack(side='left', padx=5)
tk.Radiobutton(radiobuttons_frame, text="Shrani v datoteko", variable=output_var, value="file").pack(side='left', padx=5)

# Radio gumbi za izbiro protokola
protocol_var = tk.StringVar(value="tcp")
protocol_frame = tk.Frame(root)
protocol_frame.grid(row=5, column=0, columnspan=2, pady=(2, 2), padx=(100, 0))

tk.Radiobutton(protocol_frame, text="TCP", variable=protocol_var, value="tcp").pack(side='left', padx=5)
tk.Radiobutton(protocol_frame, text="UDP", variable=protocol_var, value="udp").pack(side='left', padx=5)

# Gumb za generiranje ukazov
generate_button = tk.Button(root, text="Generiraj kodo", command=generate_commands)
generate_button.grid(row=6, column=0, columnspan=2, padx=(100, 0), pady=(5, 2))

# Izhodni okvir
output_text = tk.Text(root, height=20, width=135)
output_text.grid(row=7, column=0, columnspan=2, padx=5, pady=(2, 5))

# Dodatno tekstovno območje za izpis brez post-up/post-down
console_output_text = tk.Text(root, height=10, width=135)
console_output_text.grid(row=8, column=0, columnspan=2, padx=5, pady=(2, 5))

# Zaženi GUI
root.mainloop()
