#=> External files  
import tkinter as tk
#from tkinter import*
from tkinter import filedialog,messagebox,simpledialog
import os
import webbrowser
from tkinter.ttk import Combobox

## Main Section 
class π_editor:
    __root = tk.Tk()
    
    __root.geometry('1000x700')
    __xscrollbar = tk.Scrollbar(__root, orient=tk.HORIZONTAL)
    __yscrollbar = tk.Scrollbar(__root, orient=tk.VERTICAL)    
    __text_area = tk.Text(__root, width=1000,height =700,                                          
                                          font="bold",
                                          wrap=tk.NONE,xscrollcommand=__xscrollbar.set,
                                          yscrollcommand=__yscrollbar.set,
                                          insertontime=600
                                          )
    
    __line_bar = tk.Text(__root,height=700,state="disabled",font="bold",
                         yscrollcommand=__yscrollbar.set)
#    ,fg="White",bg="#3F3D3D"
#-------------------------------------------------------------------# 
### menu      
    __main_menu = tk.Menu(__root)
    __root.config(menu = __main_menu)
    
    __file_menu = tk.Menu(__main_menu,tearoff=False)
    __edit_menu = tk.Menu(__main_menu,tearoff=False)
    __about_menu = tk.Menu(__main_menu,tearoff=False)
#-------------------------------------------------------------------# 
### toolbar    
    __toolbar = tk.Frame(__root,bg="#eeeeee")
 

#-------------------------------------------------------------------# 
### STATUS BAR    
    status = tk.Label(__root,text=" Status |",anchor=tk.W,bd=3,relief=tk.SUNKEN)
    status.pack(side=tk.BOTTOM,fill=tk.X)
#-------------------------------------------------------------------# 
### class variables
    __file_name = None
    __line_num = 1
    
    def __init__(self):       
        self.__root.title("Untitled  π-editor")
        self.__root.iconbitmap(r"icons/icon.ico")
#-------------------------------------------------------------------#         
### Themes at opening 
        try :
            with open('CONFIG/TextAreaConfig.dat','r') as f:
                for line in f:                
                    BG,FG = line.split(",")
                self.__text_area.config(bg=BG,fg=FG)
        except:
            self.__text_area.config(bg="#2a2a2a",fg="whitE")
        
        try :
            with open('CONFIG/EditorConfig.dat','r') as f:
                for line in f:                
                    BG,FG = line.split(",")
                self.__line_bar.config(bg=BG,fg=FG)
        except:
            self.__line_bar.config(bg="#3F3D3D",fg="whitE")
                                    
        try :
            with open('CONFIG/CursorColorConfig.dat','r') as f:
                for line in f:                
                    self.__text_area.config(insertbackground=line)
        except:
            self.__text_area.config(insertbackground="Orange")
                                    
        try :
            with open('CONFIG/CursorWidthConfig.dat','r') as f:
                for line in f:                                    
                    self.__text_area.config(insertwidth = line)
        except:
            self.__text_area.config(insertwidth = 2)
                                    
        try :
            with open('CONFIG/LineBarWidthConfig.dat','r') as f:
                for line in f:                                    
                    self.__line_bar.config(width=line)
        except:
            self.__line_bar.config(width=4)                             
                                
#-------------------------------------------------------------------#                                     
        self.line_inc()                          

#-------------------------------------------------------------------#        
### MENU SECTION 
        
        #=> file menu 
        self.__main_menu.add_cascade(label="File",menu=self.__file_menu)
        self.__file_menu.add_command(label="New       Ctrl+N",command = self.new_file)
        self.__file_menu.add_command(label="Open      Ctrl+O",command=self.open_file)
        self.__file_menu.add_separator()
        self.__file_menu.add_command(label="Save       Ctrl+S",command=self.save)
        self.__file_menu.add_command(label="Save as   Ctrl+Alt+S",command=self.save_as)               
        self.__file_menu.add_separator()
        self.__file_menu.add_command(label="Quit         Alt+F4",command=self.exit)#
        
        # => Edit menu         
        self.__main_menu.add_cascade(label="Edit",menu=self.__edit_menu)
        self.__edit_menu.add_command(label="Undo        Ctrl+Z",command=self.undo)
        self.__edit_menu.add_command(label="Redo        Ctrl+Y",command=self.redo)
        self.__edit_menu.add_separator()
        self.__edit_menu.add_command(label="Cut           Ctrl+X",command=self.cut)
        self.__edit_menu.add_command(label="Copy        Ctrl+C",command=self.copy)
        self.__edit_menu.add_command(label="Paste        Ctrl+V",command=self.paste)
        self.__edit_menu.add_command(label="Select all  Ctrl+A",command=self.select_all)
        self.__edit_menu.add_separator()
        self.__edit_menu.add_command(label="Find           Ctrl+F",command=self.find)
        self.__edit_menu.add_command(label="Replace     Ctrl+R",command=self.replace)
        
        # =>Run
        self.__main_menu.add_cascade(label="Run",command=self.run)
        
        # =>Console
        self.__main_menu.add_cascade(label="Console",command=self.console)
        
        # =>Options 
        self.__main_menu.add_cascade(label="Setting",command=self.setting)
        
        # => help 
        self.__main_menu.add_cascade(label="Help",command=self.help)
       
        # =>About        
        self.__main_menu.add_cascade(label="About",menu= self.__about_menu)
        self.__about_menu.add_command(label="About π-editor",command=self.about)
        self.__about_menu.add_command(label="About us",command=self.about_us) 
        
#-------------------------------------------------------------------#
### TOOLBAR SECTION
        
        new_img = tk.PhotoImage(file='icons/new.png')        
        new_btn = tk.Button(self.__toolbar,image=new_img,width=40,height=40,bg="white",command=self.new_file)
        new_btn.image = new_img
        new_btn.pack(side=tk.LEFT,padx=(2,0),pady=0.3)
        
        open_img = tk.PhotoImage(file='icons/open.png')
        open_btn = tk.Button(self.__toolbar,image=open_img,width=40,height=40,bg="white",command=self.open_file)
        open_btn.image = open_img
        open_btn.pack(side=tk.LEFT)
        
        save_img = tk.PhotoImage(file='icons/save.png')
        save_btn = tk.Button(self.__toolbar,image=save_img,width=40,height=40,bg="white",command=self.save)
        save_btn.image = save_img                  
        save_btn.pack(side=tk.LEFT)
        
        save_as_img = tk.PhotoImage(file='icons/save_as.png')
        save_as_btn = tk.Button(self.__toolbar,image=save_as_img,width=40,height=40,bg="white",command=self.save_as)
        save_as_btn.image = save_as_img                     
        save_as_btn.pack(side=tk.LEFT)
        
        cut_img = tk.PhotoImage(file='icons/cut.png')
        cut_btn = tk.Button(self.__toolbar,image=cut_img,width=40,height=40,bg="white",command=self.cut)
        cut_btn.image = cut_img                     
        cut_btn.pack(side=tk.LEFT,padx=(2,0))
        
        copy_img = tk.PhotoImage(file='icons/copy.png')
        copy_btn = tk.Button(self.__toolbar,image=copy_img,width=40,height=40,bg="white",command=self.copy)
        copy_btn.image = copy_img                     
        copy_btn.pack(side=tk.LEFT)
        
        paste_img = tk.PhotoImage(file='icons/paste.png')
        paste_btn = tk.Button(self.__toolbar,image=paste_img,width=40,height=40,bg="white",command=self.paste)
        paste_btn.image = paste_img                     
        paste_btn.pack(side=tk.LEFT)
        
        find_img = tk.PhotoImage(file='icons/find.png')
        find_btn = tk.Button(self.__toolbar,image=find_img,width=40,height=40,bg="white",command=self.find)
        find_btn.image = find_img                     
        find_btn.pack(side=tk.LEFT,padx=(2,0))
        
        replace_img = tk.PhotoImage(file='icons/replace.png')
        replace_btn = tk.Button(self.__toolbar,image=replace_img,width=40,height=40,bg="white",command=self.replace)
        replace_btn.image = replace_img                    
        replace_btn.pack(side=tk.LEFT)
       
        run_img = tk.PhotoImage(file='icons/run.png')
        run_btn = tk.Button(self.__toolbar,image=run_img,width=40,height=40,bg="white",command=self.run)
        run_btn.image = run_img                 
        run_btn.pack(side=tk.LEFT,padx=(2,0))
       
        console_img = tk.PhotoImage(file='icons/console.png')
        console_btn = tk.Button(self.__toolbar,image=console_img,width=40,bg="white",height=40,command=self.console)
        console_btn.image = console_img                     
        console_btn.pack(side=tk.LEFT)
        
        option_img = tk.PhotoImage(file='icons/option.png')
        option_btn = tk.Button(self.__toolbar,image=option_img,width=40,height=40,bg="white",command=self.setting)
        option_btn.image = option_img                    
        option_btn.pack(side=tk.LEFT)
        
        self.__toolbar.pack(side=tk.TOP,fill=tk.X)
        
#-------------------------------------------------------------------#        
### key binding

        self.__text_area.bind("<Return>",self.line_inc)
        self.__text_area.bind("<Control-n>",self.new_file)
        self.__text_area.bind("<Control-N>",self.new_file)
        
        self.__text_area.bind("<Control-o>",self.open_file)
        self.__text_area.bind("<Control-O>",self.open_file)
        
        self.__text_area.bind("<Control-s>",self.save)
        self.__text_area.bind("<Control-S>",self.save)
        
        self.__text_area.bind("<Control-Alt-s>",self.save_as)
        self.__text_area.bind("<Control-Alt-S>",self.save_as)
        
        self.__text_area.bind("<Alt-F4>",self.exit)
        
        self.__text_area.bind("<F5>",self.run)
        self.__text_area.bind("<Control-F5>",self.console)
        self.__text_area.bind("<Button-3>",self.popup_menu)
                
        self.__text_area.bind("<Control-f>",self.find)
        self.__text_area.bind("<Control-F>",self.find)
        
        self.__text_area.bind("<Control-r>",self.replace)
        self.__text_area.bind("<Control-R>",self.replace) 
        self.__text_area.bind('<Shift-">',self.shift_q)
        self.__text_area.bind("<'>",self.shift_sq)
        self.__text_area.bind('<Shift-(>',self.shift_p)
        self.__text_area.bind('<Shift-{>',self.shift_c)
        self.__text_area.bind('<[>',self.shift_s)
        self.__text_area.bind('<Shift-KeyPress-< >',self.shift_a)
        self.__text_area.bind('<Shift-KeyPress-:>',self.shift_i)
        
        self.__root.bind("<MouseWheel>", self.mousewheel)
        
#        self.__text_area.bind("<Control-z>",self.undo)
#        self.__text_area.bind("<Control-Z>",self.undo)
#        
#        self.__text_area.bind("<Control-y>",self.redo)
#        self.__text_area.bind("<Control-Y>",self.redo)
#        
#        self.__text_area.bind("<Control-x>",self.cut)
#        self.__text_area.bind("<Control-X>",self.cut)
#        
#        self.__text_area.bind("<Control-c>",self.copy)
#        self.__text_area.bind("<Control-C>",self.copy)
#        
#        self.__text_area.bind("<Control-v>",self.paste)
#        self.__text_area.bind("<Control-V>",self.paste)
        
#        self.__text_area.bind("<Control-a>",self.select_all)
#        self.__text_area.bind("<Control-A>",self.select_all)
        
                               
#-------------------------------------------------------------------# 
### Scroll BAR
               
        self.__xscrollbar.config(command=self.__text_area.xview)
        self.__xscrollbar.pack(side=tk.BOTTOM,fill=tk.X)
        
        self.__yscrollbar.config(command=self.yview)
        self.__yscrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
#-------------------------------------------------------------------#  
### FUNCTIONS SECTION
    def a(self,*args):
        pass
#        print(self.__text_area.index(tk.INSERT))
    def mousewheel(self,event):
        self.__line_bar.yview_scroll(int(-1*(event.delta/10)),"units")
        self.__text_area.yview_scroll(int(-1*(event.delta/10)),"units")       
        return "break"

    def yview(self,*args):        
        self.__line_bar.yview(*args)
        self.__text_area.yview(*args)
        return "break"
                
    def line_inc(self,*args):
        self.__line_bar.config(state='normal')
        if self.__line_num ==1:
            self.__line_bar.insert("end",f"{self.__line_num}")
        else:
            self.__line_bar.insert("end",f"\n{self.__line_num}")
            self.__line_bar.delete("end")        
        self.__line_bar.see(tk.END)
            
        self.__line_bar.config(state='disabled')
        self.__line_num += 1
        
    def shift_p(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,"()")
        k = p.split(".")
        p = f"{k[0]}"+"."+f"{int(k[1])+1}"
        self.__text_area.mark_set(tk.INSERT,p)        
        return "break"
        
    
    def shift_c(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,"{}")
        k = p.split(".")
        p = f"{k[0]}"+"."+f"{int(k[1])+1}"
        self.__text_area.mark_set(tk.INSERT, p)
        return "break"
    
    def shift_s(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,'[]')
        k = p.split(".")
        p = f"{k[0]}"+"."+f"{int(k[1])+1}"
        self.__text_area.mark_set(tk.INSERT, p)
        return "break"
    
    def shift_q(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,'\"\"')
        k = p.split(".")
        p = f"{k[0]}"+"."+f"{int(k[1])+1}"
        self.__text_area.mark_set(tk.INSERT, p)
        return "break"
    
    def shift_sq(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,"\'\'")
        k = p.split(".")
        p = f"{k[0]}"+"."+f"{int(k[1])+1}"
        self.__text_area.mark_set(tk.INSERT, p)
        return "break"
    
    def shift_a(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,"<>")
        k = p.split(".")
        p = f"{k[0]}"+"."+f"{int(k[1])+1}"
        self.__text_area.mark_set(tk.INSERT, p)
        return "break"
    
    def shift_i(self,*args):
        p= self.__text_area.index(tk.INSERT)
        self.__text_area.insert(p,":\n"+"\t")
        self.line_inc()
        return "break"
    
    def popup_menu(self,event):
        popup = tk.Menu(self.__root, tearoff=0)     
        popup.add_command(label="Run           F5",command=self.run)
        popup.add_command(label="Console    Ctrl+F5",command=self.console)
        popup.add_separator()
        popup.add_command(label="Undo        Ctrl+Z",command=self.undo)
        popup.add_command(label="Redo        Ctrl+Y",command=self.redo)
        popup.add_separator()
        popup.add_command(label="Cut           Ctrl+X",command=self.cut)
        popup.add_command(label="Copy        Ctrl+C",command=self.copy)
        popup.add_command(label="Paste        Ctrl+V",command=self.paste)
        popup.add_command(label="Select all  Ctrl+A",command=self.select_all)
        try:                       
                popup.tk_popup(event.x_root+80,event.y_root+20,0)                        
        finally:        
            popup.grab_release()
        
    def title(self):
        t = (self.__file_name.name).split("/")
        self.__root.title(f"{t[-1]}  π-editor")
        self.status.config(text=f" Status | {self.__file_name.name}")
        
    def new_file(self,*args):
        if len(self.__text_area.get("1.0",tk.END+"-1c")) >0 or self.__file_name != None :
            option = messagebox.askyesnocancel("save","Do you want to save it")
            if option == True:
                self.save()
                self.__text_area.delete(1.0,tk.END)
                self.__root.title("Untitled  π-editor")
                self.__file_name = None
                
                self.__line_bar.config(state='normal')
                self.__line_bar.delete(1.0,tk.END) 
                self.__line_bar.config(state='disabled')
                self.__line_num = 1
                self.line_inc()
                
                self.status.config(text=f" Status |")
                                
            elif option == False:
                self.__text_area.delete(1.0,tk.END)
                self.__root.title("Untitled  π-editor")
                self.__file_name = None
                
                self.__line_bar.config(state='normal')
                self.__line_bar.delete(1.0,tk.END) 
                self.__line_bar.config(state='disabled')
                self.__line_num = 1
                self.line_inc() 
                
                self.status.config(text=f" Status |")
        
    def open_file(self,*args):
        self.__file_name = filedialog.askopenfile(parent=self.__root, title="Select a text file",
                                      filetypes=(("Python file","*.py"),("All files","*.*")))            
        if self.__file_name != None: 
            self.__text_area.delete(1.0,tk.END)
            self.__text_area.insert("1.0",self.__file_name.read())    
            self.__file_name.close()
            self.__text_area.see(tk.END)
            
            self.title()
            self.status.config(text=f"| Status | {self.__file_name.name}")
            
            self.__line_bar.config(state='normal')
            self.__line_bar.delete(1.0,tk.END) 
            self.__line_bar.config(state='disabled')
            self.__line_num = 1
            
            with open(f"{self.__file_name.name}","r") as f:
                line = f.readlines()
                for i in line:                    
                    self.line_inc()
            
    def save(self,*args):
        if self.__file_name == None: 
           self.save_as();
           if self.__file_name == None: 
                self.__file_name = None
           else:                   
                file = open(self.__file_name.name,"w") 
                file.write(self.__text_area.get("1.0",tk.END)) 
                file.close()
           
        else: 
            file = open(self.__file_name.name,"w") 
            file.write(self.__text_area.get("1.0",tk.END)) 
            file.close()
            self.title()
            
            
    def save_as(self,*args):                            
        self.__file_name = filedialog.asksaveasfile(mode="w",initialfile='Untitled.py',defaultextension=".py",
                                        filetypes=(("Python File","*.py"),("All files","*.*"))) 
        if self.__file_name != None:
            data =  self.__text_area.get("1.0",tk.END+"-1c")
            self.__file_name.write(data)
            self.__file_name.close()
            self.title() 
            
    def exit(self,*args):
        if messagebox.showinfo("Quit","Are you sure want to quit"):
            self.__root.destroy()
            
    def undo(self,*args):
        self.__text_area.event_generate("<<Undo>>") 
        return "break"

    def redo(self,*args):
        self.__text_area.event_generate("<<Redo>>")
        return "break"
        
    def cut(self,*args):
        self.__text_area.event_generate("<<Cut>>")
        
    def copy(self,*args):
        self.__text_area.event_generate("<<Copy>>")
        
    def paste(self,*args):
        self.__text_area.event_generate("<<Paste>>")
        
    def select_all(self,*args):
        self.__text_area.tag_add('sel', '1.0', 'end')
        
        
    def find(self,*args):
        if len(self.__text_area.get("1.0",tk.END+"-1c")) >0:
            find_string = simpledialog.askstring("Find","Find what") 
            try: 
                data = self.__text_area.get("1.0",tk.END+"-1c")
                occurance = data.upper().count(find_string.upper())
                if occurance == 1:
                    messagebox.showinfo("Results",f"{find_string} occured once ")
                elif occurance >1:
                    messagebox.showinfo("Results",f"{find_string} occured {occurance} times")
                else :
                    messagebox.showerror("Results","Not found")
            except: 
                pass
        else:
            messagebox.showerror("Error","Empty File!!")  
    
    def replace(self,*args):
          
        if len(self.__text_area.get("1.0",tk.END+"-1c")) >0:             
            replace_win = tk.Toplevel()
            replace_win.iconbitmap(r"icons/icon.ico")
            replace_win.title("REPLACE")
            replace_win.geometry('280x180')
            replace_win.resizable(width=False,height=False)
            
            def not_found(error):
                messagebox.showerror("ERROR",error)
                
            def replace_next():
                string = old.get()
                data = self.__text_area.get("1.0",tk.END+"-1c")
                if string not in data:
                    messagebox.showerror("Old String Not Found")
               
                elif old.get() == "":
                    messagebox.showerror("Enter Old String")
                
                elif new.get() == "":
                    messagebox.showerror("Enter New String")
                else:
                    new_data = data.replace(old.get(),new.get(),1)
                    self.__text_area.delete(1.0,tk.END)
                    self.__text_area.insert(tk.END,new_data)
                    
            def replace_all():
                string = old.get()
                data = self.__text_area.get("1.0",tk.END+"-1c")
                if string not in data:
                    messagebox.showerror("Old String Not Found")
               
                elif old.get() == "":
                    messagebox.showerror("Enter Old String")
                
                elif new.get() == "":
                    messagebox.showerror("Enter New String")
                else:
                    new_data = data.replace(old.get(),new.get())
                    self.__text_area.delete(1.0,tk.END)
                    self.__text_area.insert(tk.END,new_data)
               
            old_label = tk.Label(replace_win,text="Old String : ")
            old_label.place(x=10,y=20)
            old = tk.Entry(replace_win)
            old.place(x=100,y=20) 
            
            new_label = tk.Label(replace_win,text="New String : ")
            new_label.place(x=10,y=65)
            new = tk.Entry(replace_win)
            new.place(x=100,y=65)
                        
            replace_all_btn = tk.Button(replace_win,text='Replace/Find next',command=replace_next)
            replace_all_btn.place(x=20,y=110) 
            
            replace_btn = tk.Button(replace_win,text='Replace All',command=replace_all)
            replace_btn.place(x=175,y=110)
             
        else:
            messagebox.showerror("Error","Empty File!!")
            
    def run(self,*args):
        if self.__file_name !=None:
            if len(self.__text_area.get("1.0",tk.END+"-1c")) >0:
                self.save();
                bat_file = open("run.bat","w")
                bat_file.write(f"@echo off\nstart cmd.exe /k python {self.__file_name.name} ")
                bat_file.close()    
                os.system("run.bat")
            else :
                messagebox.showerror("Error","Empty File!!")
        else :
                choice = messagebox.askyesno("Save Before Run ","\nOK to save ?")
                if(choice == True):
                    self.save_as()
                    self.run()
                    
    def console(self,*args):
        os.system("python.exe")
    
                
    def setting(self):
        setting_win = tk.Toplevel()
        setting_win.iconbitmap(r"icons/icon.ico")
        setting_win.geometry('400x600')
        setting_win.resizable(width=False,height=False)
        setting_win.title("SETTINGS")
            
#--------------------------------------#  
        editor = tk.Frame(setting_win)
        seprate = tk.Label(setting_win,text="____________________________________________________\
______________").place(x=0,y=0)
        option_title = tk.Label(setting_win,text="Editor Setting").place(x=10,y=5)
        option_title = tk.Label(setting_win,text="Line Bar : ").place(x=10,y=40)
        
        editor_color_scheme= {"Light":"White,Black",
                              "Dark":"#3F3D3D,White"
                             }
        editor_theme = []
        for i in editor_color_scheme.keys():
            editor_theme.append(i)        
        selected_editor_theme = tk.StringVar()
        color_choices = Combobox(setting_win,value = editor_theme,width=30,textvariable=selected_editor_theme)
        color_choices.place(x=100,y=40)
        
        option_title = tk.Label(setting_win,text="Cursor : ").place(x=10,y=80)
        cursor_colors = ["Red","Blue","Green","Orange","Pink","White","Black"]
        selected_cursor_color = tk.StringVar()
        cursor_color_choices = Combobox(setting_win,value = cursor_colors,width=30,textvariable=selected_cursor_color)
        cursor_color_choices.place(x=100,y=80) 
        
        option_title = tk.Label(setting_win,text="Line Bar Width : ").place(x=10,y=120)        
        editor_choice_width = ["1","2","3","4","5","6","7","8"]
        selected_line_bar_width = tk.StringVar()
        line_bar_choice = Combobox(setting_win,value = editor_choice_width,width=5,textvariable=selected_line_bar_width)
        line_bar_choice.place(x=125,y=120)
        
        option_title = tk.Label(setting_win,text="Cursor Width : ").place(x=200,y=120)        
        selected_cursor_width = tk.StringVar()
        cursor_choices = Combobox(setting_win,value = editor_choice_width,width=5,textvariable=selected_cursor_width)
        cursor_choices.place(x=300,y=120)
        
        editor.pack()
#--------------------------------------#        
        theme = tk.Frame(setting_win)
        seprate = tk.Label(setting_win,text="____________________________________________________\
______________").place(x=0,y=160)
        option_title = tk.Label(setting_win,text="Text Area Setting").place(x=10,y=165)
        
        option_title = tk.Label(setting_win,text="Themes : ").place(x=10,y=200)
        color_schemes = {
                        "Light":"#FFFFFF,#000000",
                        "Light code Red":"white,#FF0000",
                        "Light code Green":"white,#16C60C",
                        "Light code Blue":"white,#00EBFE",
                        "Light code Orange":"white,#FF7000",
                        "Sky":"#14C2F7,White",
                        "Mid Night":"#2a2a2a,White",
                        "Mid Night Orange":"#2a2a2a,#FF7000",
                        "Dark":"#0C0C0C,White",
                        "Dark code Red":"#0C0C0C,#FF0000",
                        "Dark code Green":"#0C0C0C,#16C60C",
                        "Dark code Blue":"#0C0C0C,#00EBFE",
                        "Dark code Orange":"#0C0C0C,#ffaf1a"
                        }
        choices = []
        for i in color_schemes.keys():
            choices.append(i) 
        selected_theme = tk.StringVar()
        color_choices = Combobox(setting_win,value=choices,width=30,textvariable=selected_theme)
        
        color_choices.place(x=100,y=200)                       
        theme.pack()
#--------------------------------------#        
        cmd = tk.Frame(setting_win)
        seprate = tk.Label(setting_win,text="____________________________________________________\
______________").place(x=0,y=240)
        option_title = tk.Label(setting_win,text="CMD Setting").place(x=10,y=245) 
        
        cmd_choices= ["0-Black","1-Blue","2-Green","3-Aqua",
                  "4-red","5-Purple","6-Yellow","7-White",
                  "8-Gray","9-Light Blue","A-Light Green","B-Light Aqua",
                  "C-Light Red","D-Light purple","E-Light Yellow","F-Bright White"]
        
        option_title = tk.Label(setting_win,text="Background: ").place(x=10,y=280)
        selected_cmd_back = tk.StringVar()             
        font_style = Combobox(setting_win,value=cmd_choices,width=30,text=selected_cmd_back)
        font_style.place(x=100,y=280)
        
        option_title = tk.Label(setting_win,text="Text : ").place(x=10,y=315)
        selected_cmd_text = tk.StringVar()                   
        font_style = Combobox(setting_win,value=cmd_choices,width=30,text=selected_cmd_text)
        font_style.place(x=100,y=315)                       
        cmd.pack()
#--------------------------------------#
        seprate = tk.Label(setting_win,text="____________________________________________________\
______________").place(x=0,y=350)
        option_title = tk.Label(setting_win,text="Note*").place(x=10,y=355)
        note1 = tk.Label(setting_win,text="-> Background Color And Text Color Can't Be Same").place(x=10,y=395)
        note2 = tk.Label(setting_win,text="-> Press Apply To See Changes").place(x=10,y=430)
        note3 = tk.Label(setting_win,text="-> Press OK To Save Changes").place(x=10,y=465)
        note4 = tk.Label(setting_win,text="-> Press Cancel To Discard Changes").place(x=10,y=500)
        
#--------------------------------------#
        def apply(): 
            if selected_theme.get() != "":
                background_color,foreground_color  = color_schemes[selected_theme.get()].split(",")
                self.__text_area.config(background=background_color, fg=foreground_color)
            else :
                pass
            
            if selected_editor_theme.get() != "":
                background_color,foreground_color  = editor_color_scheme[selected_editor_theme.get()].split(",")
                self.__line_bar.config(background=background_color, fg=foreground_color)
            else :
                pass
            
            if selected_cursor_color.get() != "": 
                self.__text_area.config(insertbackground = selected_cursor_color.get())
            else :
                pass
           
            if selected_line_bar_width.get() != "":                
                self.__line_bar.config(width= selected_line_bar_width.get())
            else :
                pass
            
            if selected_cursor_width.get() != "":                
                self.__text_area.config(insertwidth=selected_cursor_width.get())
            else :
                pass
            
            if (selected_cmd_back.get() != "") and (selected_cmd_text.get() !=""):
                b= selected_cmd_back.get().split("-")[0]
                t= selected_cmd_text.get().split("-")[0]
                bat_file = open("testconfig.bat","w")
                bat_file.write(f'@echo off\nstart cmd.exe /k color {b}{t}')
                bat_file.close()    
                os.system("testconfig.bat")
            else:
                pass
        
        def ok():
            apply()
            if selected_theme.get() != "":
                data = color_schemes[selected_theme.get()]
                file = open("CONFIG\TextAreaConfig.dat","w")
                file.write(data)
                file.close
            else :
                pass
            if (selected_cmd_back.get() != "") and (selected_cmd_text.get() !=""):
                b= selected_cmd_back.get().split("-")[0]
                t= selected_cmd_text.get().split("-")[0]
                bat_file = open("cmdconfig.bat","w")
                bat_file.write(f'@echo off\nstart cmd.exe /c reg add "HKCU\Software\Microsoft\Command Processor" /v Autorun /t REG_SZ /d "color {b}{t}" /f')
                bat_file.close()    
                os.system("cmdconfig.bat")            
            else:
                pass
            
            if selected_editor_theme.get() != "":
                data  = editor_color_scheme[selected_editor_theme.get()]
                file = open("CONFIG\EditorConfig.dat","w")
                file.write(data)
                file.close
            else :
                pass
            
            if selected_cursor_color.get() != "": 
                file = open("CONFIG\CursorColorConfig.dat","w")
                file.write(selected_cursor_color.get())
                file.close
            else :
                pass
           
            if selected_line_bar_width.get() != "":                
                file = open("CONFIG\LineBarWidthConfig.dat","w")
                file.write(selected_line_bar_width.get())
                file.close
            else :
                pass
            
            if selected_cursor_width.get() != "":                
                file = open("CONFIG\CursorWidthConfig.dat","w")
                file.write(selected_cursor_width.get())
                file.close
            else :
                pass
            cancel()    
        def cancel():            
                setting_win.destroy()
        
        ok_btn = tk.Button(setting_win,text="Ok",width=10,command=ok)
        ok_btn.place(x=100,y=550)
        apply_btn = tk.Button(setting_win,text="Apply",width=10,command=apply)
        apply_btn.place(x=200,y=550)
        cancel_btn = tk.Button(setting_win,text="Cancel",width=10,command=cancel)
        cancel_btn.place(x=300,y=550)       
#--------------------------------------#     
    def help(self):
        file = open("CONFIG\webHelp.dat","r")
        url = file.read()
        file.close()
        webbrowser.open(url)
        
    def about(self):     
        about_win = tk.Toplevel()
        about_win.iconbitmap(r"icons/icon.ico")
        about_win.geometry('300x400')
        about_win.resizable(width=False,height=False)
        about_win.title("ABOUT")
        
        about_title = tk.Label(about_win,text="π-editor\n")               
        about_title.pack(side=tk.TOP, fill=tk.X,pady=10)
        
        about_img = tk.PhotoImage(file='icons/about.png')        
        about_con = tk.Label(about_win,image=about_img)
        about_con .image = about_img
        about_con.pack(side=tk.TOP)
        
        about_des = tk.Label(about_win,text="π-editor v 1.0.5\n\
Python's Development Environment\n\
Created By A Group Of Four Geeks :)")               
        about_des.pack(fill=tk.X,pady=20)
        
    def about_us(self):
        
        file = open("CONFIG\web.dat","r")
        url = file.read()
        file.close()
        webbrowser.open(url)
                   
    def π_editor_run(self):
        self.__line_bar.pack(fill=tk.Y,side="left")
        self.__text_area.pack(fill=tk.BOTH,expand='yes')        
        self.__root.mainloop()
           
#-------------------------------------------------------------------#
var = π_editor()
var.π_editor_run()