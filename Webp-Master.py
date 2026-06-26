import os
import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

# -----------------------------------------------------------
# App Configuration & Styling
# -----------------------------------------------------------
ctk.set_appearance_mode("Dark")  # Options: "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class WebPConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("WebP Master v1.0.0 - Pro Image Optimizer")
        self.geometry("800x750")
        self.minsize(750, 700)
        
        # State Variables
        self.input_files = []
        self.output_directory = ctk.StringVar(value=os.path.expanduser("~"))
        self.is_converting = False
        
        # Power Rename Variables
        self.find_var = ctk.StringVar()
        self.replace_var = ctk.StringVar()
        self.prefix_var = ctk.StringVar()
        self.suffix_var = ctk.StringVar()
        self.casing_var = ctk.StringVar(value="Keep Original")
        self.seq_var = ctk.BooleanVar(value=False)
        self.seq_start_var = ctk.StringVar(value="1")
        
        # Build UI Components
        self.build_ui()

    def build_ui(self):
        """Constructs the Grid Layout and UI Elements"""
        
        # --- Configure Grid System ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # The files list takes remaining space

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title_label = ctk.CTkLabel(header_frame, text="WebP Master", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(side="left")
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Advanced Batch Optimizer", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle_label.pack(side="left", padx=10, pady=(8, 0))

        # --- Section 1: Input Files ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=1)

        btn_add_files = ctk.CTkButton(input_frame, text="+ Select Images", command=self.add_files)
        btn_add_files.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        btn_clear_files = ctk.CTkButton(input_frame, text="Clear List", fg_color="transparent", border_width=1, command=self.clear_files)
        btn_clear_files.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Scrollable frame for file list
        self.file_list_frame = ctk.CTkScrollableFrame(input_frame, label_text="Selected Files")
        self.file_list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

        # --- Section 2: Tabbed Interface (Compression & Rename) ---
        self.tabview = ctk.CTkTabview(self, height=220)
        self.tabview.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        tab_comp = self.tabview.add("Compression")
        tab_ren = self.tabview.add("Power Rename")

        # --- Compression Tab ---
        tab_comp.grid_columnconfigure((0, 1), weight=1)

        # Quality Slider
        self.quality_label = ctk.CTkLabel(tab_comp, text="Quality: 80%")
        self.quality_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        self.quality_slider = ctk.CTkSlider(tab_comp, from_=1, to=100, command=self.update_quality_label)
        self.quality_slider.set(80)
        self.quality_slider.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Method Slider (Engine Effort)
        self.method_label = ctk.CTkLabel(tab_comp, text="Compression Engine Effort: 6 (Best/Slowest)")
        self.method_label.grid(row=0, column=1, padx=10, pady=(5, 0), sticky="w")
        self.method_slider = ctk.CTkSlider(tab_comp, from_=0, to=6, number_of_steps=6, command=self.update_method_label)
        self.method_slider.set(6)
        self.method_slider.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Checkboxes
        checkbox_frame = ctk.CTkFrame(tab_comp, fg_color="transparent")
        checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.lossless_var = ctk.BooleanVar(value=False)
        self.chk_lossless = ctk.CTkCheckBox(checkbox_frame, text="Lossless Format", variable=self.lossless_var)
        self.chk_lossless.pack(side="left", padx=(0, 20))
        
        self.exif_var = ctk.BooleanVar(value=True)
        self.chk_exif = ctk.CTkCheckBox(checkbox_frame, text="Keep EXIF/Metadata", variable=self.exif_var)
        self.chk_exif.pack(side="left")

        # --- Power Rename Tab ---
        tab_ren.grid_columnconfigure((1, 3), weight=1)
        
        # Attach traces to variables to update live preview
        for var in (self.find_var, self.replace_var, self.prefix_var, self.suffix_var, self.seq_start_var):
            var.trace_add("write", self.update_preview)

        # Row 0: Find & Replace
        ctk.CTkLabel(tab_ren, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(tab_ren, textvariable=self.find_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(tab_ren, text="Replace:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(tab_ren, textvariable=self.replace_var).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Row 1: Prefix & Suffix
        ctk.CTkLabel(tab_ren, text="Prefix:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(tab_ren, textvariable=self.prefix_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(tab_ren, text="Suffix:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ctk.CTkEntry(tab_ren, textvariable=self.suffix_var).grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Row 2: Casing & Numbering
        ctk.CTkLabel(tab_ren, text="Casing:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        casing_menu = ctk.CTkOptionMenu(tab_ren, variable=self.casing_var, values=["Keep Original", "lowercase", "UPPERCASE"], command=self.update_preview)
        casing_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        seq_frame = ctk.CTkFrame(tab_ren, fg_color="transparent")
        seq_frame.grid(row=2, column=2, columnspan=2, sticky="w")
        ctk.CTkCheckBox(seq_frame, text="Add Number", variable=self.seq_var, command=self.update_preview).pack(side="left", padx=5)
        ctk.CTkLabel(seq_frame, text="Start at:").pack(side="left", padx=5)
        ctk.CTkEntry(seq_frame, textvariable=self.seq_start_var, width=50).pack(side="left", padx=5)

        # Row 3: Live Preview
        preview_frame = ctk.CTkFrame(tab_ren, fg_color="#2b2b2b", corner_radius=5)
        preview_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=(10, 5), sticky="ew")
        self.preview_label = ctk.CTkLabel(preview_frame, text="Preview: original_name.webp -> original_name.webp", text_color="#a3a3a3")
        self.preview_label.pack(padx=10, pady=5)

        # --- Section 3: Output & Execution ---
        action_frame = ctk.CTkFrame(self)
        action_frame.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="ew")
        action_frame.grid_columnconfigure(1, weight=1)

        # Output Directory
        ctk.CTkLabel(action_frame, text="Save to:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_output = ctk.CTkEntry(action_frame, textvariable=self.output_directory, state="readonly")
        self.entry_output.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        btn_browse_out = ctk.CTkButton(action_frame, text="Browse", width=80, command=self.select_output_dir)
        btn_browse_out.grid(row=0, column=2, padx=10, pady=10)

        # Convert Button
        self.btn_convert = ctk.CTkButton(action_frame, text="START CONVERSION", font=ctk.CTkFont(size=16, weight="bold"), height=50, command=self.start_conversion)
        self.btn_convert.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="ew")

        # Progress Bar & Status
        self.progress_bar = ctk.CTkProgressBar(action_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")
        
        self.status_label = ctk.CTkLabel(action_frame, text="Ready", text_color="gray")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=(0, 10))

        # --- Section 4: Footer / Developer Info ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        version_label = ctk.CTkLabel(footer_frame, text="v1.0.0", text_color="gray", font=ctk.CTkFont(size=12))
        version_label.pack(side="left")
        
        dev_label = ctk.CTkLabel(footer_frame, text=" | Developed by Mayur Sharma", text_color="gray", font=ctk.CTkFont(size=12))
        dev_label.pack(side="left")

        # Clickable GitHub Link
        btn_git = ctk.CTkButton(footer_frame, text="GitHub: geeymayur", fg_color="transparent", text_color="#4da6ff", hover_color="#2b2b2b", font=ctk.CTkFont(size=12, underline=True), width=0, command=lambda: webbrowser.open("https://github.com/geeymayur"))
        btn_git.pack(side="right", padx=(5, 0))

        # Clickable Website Link
        btn_web = ctk.CTkButton(footer_frame, text="www.mayurx.in", fg_color="transparent", text_color="#4da6ff", hover_color="#2b2b2b", font=ctk.CTkFont(size=12, underline=True), width=0, command=lambda: webbrowser.open("https://www.mayurx.in"))
        btn_web.pack(side="right", padx=5)


    # --- UI Callbacks & Logic ---

    def update_preview(self, *args):
        """Updates the Live Preview text in the Power Rename tab"""
        sample_name = "example_image_123.jpg"
        if self.input_files:
            sample_name = os.path.basename(self.input_files[0])
            
        new_base = self.generate_new_filename(sample_name, 0)
        self.preview_label.configure(text=f"Preview: {sample_name}  ->  {new_base}.webp")

    def generate_new_filename(self, original_filename, index):
        """Applies power rename rules to a filename"""
        base_name = os.path.splitext(original_filename)[0]
        
        # 1. Find and Replace
        find_text = self.find_var.get()
        replace_text = self.replace_var.get()
        if find_text:
            base_name = base_name.replace(find_text, replace_text)
            
        # 2. Text Casing
        casing = self.casing_var.get()
        if casing == "lowercase":
            base_name = base_name.lower()
        elif casing == "UPPERCASE":
            base_name = base_name.upper()
            
        # 3. Prefix and Suffix
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        base_name = f"{prefix}{base_name}{suffix}"
        
        # 4. Sequential Numbering
        if self.seq_var.get():
            try:
                start_num = int(self.seq_start_var.get() or 1)
            except ValueError:
                start_num = 1
            current_num = start_num + index
            base_name = f"{base_name}_{current_num:02d}"  # Pads with zero: _01, _02, etc.
            
        return base_name

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"Quality: {int(value)}%")

    def update_method_label(self, value):
        labels = {
            0: "0 (Fastest/Largest Size)",
            6: "6 (Best Compression/Slowest)"
        }
        text = labels.get(int(value), f"{int(value)}")
        self.method_label.configure(text=f"Compression Engine Effort: {text}")

    def add_files(self):
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
            ("All files", "*.*")
        )
        filenames = filedialog.askopenfilenames(title="Select Images to Convert", filetypes=filetypes)
        
        for f in filenames:
            if f not in self.input_files:
                self.input_files.append(f)
                
        self.refresh_file_list()

    def clear_files(self):
        self.input_files.clear()
        self.refresh_file_list()

    def refresh_file_list(self):
        # Clear existing widgets
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
            
        # Repopulate
        for i, file_path in enumerate(self.input_files):
            lbl = ctk.CTkLabel(self.file_list_frame, text=os.path.basename(file_path), anchor="w")
            lbl.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

        self.status_label.configure(text=f"{len(self.input_files)} file(s) ready.")
        self.update_preview()  # Force preview to update when files are added/cleared

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)

    def start_conversion(self):
        if not self.input_files:
            self.status_label.configure(text="Error: No files selected!", text_color="red")
            return
            
        if self.is_converting:
            return

        self.is_converting = True
        self.btn_convert.configure(state="disabled", text="CONVERTING...")
        self.progress_bar.set(0)
        
        # Start a daemon thread so the UI remains responsive during heavy processing
        threading.Thread(target=self.process_images, daemon=True).start()

    def process_images(self):
        out_dir = self.output_directory.get()
        os.makedirs(out_dir, exist_ok=True)

        total_files = len(self.input_files)
        success_count = 0

        # Retrieve user settings
        q = int(self.quality_slider.get())
        m = int(self.method_slider.get())
        is_lossless = self.lossless_var.get()
        keep_exif = self.exif_var.get()

        for idx, file_path in enumerate(self.input_files):
            try:
                # Update status
                filename = os.path.basename(file_path)
                self.status_label.configure(text=f"Converting ({idx+1}/{total_files}): {filename}", text_color="white")

                # Open and convert
                with Image.open(file_path) as img:
                    # Convert color modes if necessary (WebP needs RGB or RGBA)
                    if img.mode not in ("RGB", "RGBA"):
                        if "transparency" in img.info or img.mode in ("P", "LA"):
                            img = img.convert("RGBA")
                        else:
                            img = img.convert("RGB")

                    # Handle output naming using Power Rename rules
                    new_base_name = self.generate_new_filename(filename, idx)
                    out_path = os.path.join(out_dir, f"{new_base_name}.webp")

                    # Configuration parameters for Google's libwebp
                    save_kwargs = {
                        "format": "WEBP",
                        "quality": q,
                        "lossless": is_lossless,
                        "method": m,
                        "exact": is_lossless # Preserves RGB values in transparent areas if lossless
                    }

                    # Append EXIF metadata if requested and available
                    if keep_exif:
                        exif_data = img.info.get('exif')
                        if exif_data:
                            save_kwargs['exif'] = exif_data

                    # Perform conversion
                    img.save(out_path, **save_kwargs)
                    success_count += 1

            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")
            
            # Update Progress Bar
            progress = (idx + 1) / total_files
            self.progress_bar.set(progress)

        # Re-enable UI after completion
        self.is_converting = False
        self.btn_convert.configure(state="normal", text="START CONVERSION")
        self.status_label.configure(text=f"Done! Successfully converted {success_count} of {total_files} images.", text_color="#32a852")

# -----------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------
if __name__ == "__main__":
    app = WebPConverterApp()
    app.mainloop()