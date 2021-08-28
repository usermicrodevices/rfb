# rfb - Remote File Browser
# Copyright Max Kolosov 2007-2010 maxkolosov@inbox.ru
# http://sourceforge.net/projects/rfb/
# http://saxi.nm.ru/
# BSD license

gui_codec = 'cp1251'

import os, sys, re, cPickle
if globals()['__file__'] != sys.argv[0]:
	type_application = globals()['__file__']
	if type_application == '<frozen>':
		if os.path.isdir('lib'):
			sys.path.insert(0, 'lib')
			import encodings.ascii as ascii
			import encodings.idna as idna
elif os.path.isdir('lib'):
	sys.path.insert(0, 'lib')

from threading import Thread

try:
	import exe
except:
	import wx
else:
	import keyword, inspect

import wx.grid as gr
from wx.gizmos import TreeListCtrl
from wx.lib.rcsizer import RowColSizer
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.throbber import Throbber
from wx.py.shell import ShellFrame
from wx.lib.newevent import NewEvent
from wx.aui import AuiManager, AuiPaneInfo, AuiToolBar, AUI_TB_DEFAULT_STYLE, AUI_TB_OVERFLOW

import gettext
_ = gettext.gettext

from locale import getdefaultlocale, setlocale, LC_ALL
setlocale(LC_ALL, '')

default_fullscreen_style = wx.FULLSCREEN_NOSTATUSBAR | wx.FULLSCREEN_NOBORDER | wx.FULLSCREEN_NOCAPTION

remote_create_dir_xpm = '''16 16 3 1
  c None
X c #00FF00
. c #0000FF
  .....         
 .     .        
.       .       
.       .       
.        .....  
.             . 
.      XX      .
.      XX      .
.      XX      .
.   XXXXXXXX   .
.   XXXXXXXX   .
.      XX      .
.      XX      .
.      XX      .
 .            . 
  ............  '''
load_dir_xpm = '''16 16 4 1
  c None
X c #FFFF00
. c #9A9EF2
o c #74F5B7
  .....         
 .     .        
.       .       
.       .       
.        .....  
.             . 
.      X       .
.      X       .
.      X       .
.   o  X  o    .
.   o  X  o    .
.    o X o     .
.     oXo      .
.      o       .
 .            . 
  ............  '''
load_dir_open_xpm = '''16 16 4 1
  c None
X c #FFFF00
. c #9A9EF2
o c #74F5B7
  .....         
 .     .        
.       .       
.       .       
.        .....  
.             . 
.    ........  .
.   .    X   . .
.  .     X    ..
.  .     X     .
.  .  o  X  o  .
.  .  o  X  o  .
.  .   o X o   .
.  .    oXo    .
 .  .    o    . 
  ............  '''
send_dir_xpm = '''16 16 4 1
  c None
o c #FFFF00
. c #0000FF
X c #74F5B7
  .....         
 .     .        
.       .       
.       .       
.        .....  
.             . 
.              .
.              .
.         XX   .
.           X  .
.  ooooooooooX .
.           X  .
.         XX   .
.              .
 .            . 
  ............  '''
send_dir_open_xpm = '''16 16 4 1
  c None
o c #FFFF00
. c #0000FF
X c #74F5B7
  .....         
 .     .        
.       .       
.       .       
.        .....  
.             . 
.    ........  .
.   .        . .
.  .          ..
.  .       XX  .
.  .         X .
.  .ooooooooooX.
.  .         X .
.  .       XX  .
 .  .         . 
  ............  '''
rfb_xpm = '''16 16 4 1
  c None
. c #8000C0
o c #E00080
X c #00FF00
                
                
                
 ...  XXXX ooo  
 .  . X    o  o 
 .  . X    o  o 
 .  . X    o  o 
 ...  X    ooo  
 ..   XXX  o  o 
 . .  X    o  o 
 . .  X    o  o 
 .  . X    o  o 
 .  . X    ooo  
                
                
                '''
log_xpm = '''16 16 4 1
  c None
. c #8000C0
o c #E00080
X c #00FF00
                
                
                
 .     XX  ooo  
 .    X  X o  o 
 .    X  X o    
 .    X  X o    
 .    X  X o    
 .    X  X o    
 .    X  X o o  
 .    X  X o  o 
 .    X  X o  o 
 ....  XX  ooo  
                
                
                '''
eraser_xpm = '''16 16 5 1
  c None
O c #00FF80
. c #004040
X c #0000FF
o c #FFFF80
                
     ...        
    XXXXX       
   XXXXXXX      
  XXXXXXXXX     
 .XXXXXXXXXX    
 .XXXXXXXXXoO   
 .XXXXXXXXoOOO  
  XXXXXXXoOOOO  
   XXXXXoOOOOO  
    XXXoOOOOOO  
     XoOOOOOO   
      OOOOOO    
       OOOO     
                
                '''
throbber_xpm = '''16 16 10 1
  c None
. c #8080C0
0 c #00FF00
1 c #FF0000
2 c #FFFF00
3 c #0080C0
4 c #008080
5 c #E00080
6 c #00FFFF
7 c #0000FF
     ......     
    .111222.    
  ..11112222..  
  .0111122223.  
 .000111222333. 
.00000112233333.
.00000012333333.
.000000..333333.
.777777..444444.
.77777765444444.
.77777665544444.
 .777666555444. 
  .7666655554.  
  ..66665555..  
    .666555.    
     ......     '''
net_dir_xpm = '''32 32 26 1
  c None
. c #0000FF
% c #303134
7 c #2E3136
5 c #333539
X c #CC9900
- c #2C3138
> c #CCCCCC
# c #FFE680
@ c #FFFF00
3 c #A0A0BD
$ c #CF9C06
6 c #2F3136
1 c #666666
: c #939393
& c #B9B6AD
* c #B9B9B9
, c #767676
4 c #C0C0EC
; c #2E3238
= c #2E3239
< c #00FF00
o c #FFFF99
O c #FFFF9F
+ c #FFFFA4
2 c #868696
                                
                        .       
                        .       
     XXXXXX         .   .   .   
    XXooooXX     XXX..X . ...   
   XXooOoooXXXXXXXooo......     
   Xo+ooooOoooooooooo..@@..     
   Xooooooooooooo.....@@@@..... 
   XoooooooooooooXXXX..@@..     
   XooooooooooXXXX###.......    
   XoooooooooXX######.#$.  .    
   XooooXXXXXX######..#$.  ..   
   XoooX###############$.       
   XoooX###############X.       
   XooX################X        
   XooX###############XX        
   XooX###############X         
   XooX##############XX         
   XooX##############XX         
   XoX##############XX          
   XoX#########XXXXXX           
   XXX#####XXXXXXX%             
   X$XXXXXXXX%&***%             
    XXXXXX=-;%::::%%%%          
         %>>>>>>>>>>>>%         
  %%%%%%%%,,,,,,,,,,,,%%%%%%%%  
 %<<<<<<<%111111111111%<<<<<<<% 
 %<<<<<<<%222222222222%<<<<<<<% 
  %%%%%%%%333333333333%%%%%%%%  
         %444444444444%         
          %56777777776          
                                '''
closed_net_dir_xpm = '''32 32 24 1
  c None
& c #303134
5 c #2E3136
X c #CC9900
; c #2C3138
> c #CCCCCC
# c #FFE680
@ c #FFFF00
3 c #A0A0BD
$ c #CF9C06
% c #FF0000
1 c #666666
: c #939393
. c #0000FF
* c #B9B6AD
= c #B9B9B9
, c #767676
4 c #C0C0EC
- c #2E3239
< c #00FF00
o c #FFFF99
O c #FFFF9F
+ c #FFFFA4
2 c #868696
                                
                        .       
                        .       
     XXXXXX         .   .   .   
    XXooooXX     XXX..X . ...   
   XXooOoooXXXXXXXooo......     
   Xo+ooooOoooooooooo..@@..     
   Xooooooooooooo.....@@@@..... 
   XoooooooooooooXXXX..@@..     
   XooooooooooXXXX###.......    
   XoooooooooXX######.#$.  .    
   XooooXXXXXX######..#$.  ..   
   XoooX###############$.       
   XoooX###############X.       
   XooX################X        
   XooX###############XX        
   XooX###############X         
   XooX##############XX         
   XooX##############XX         
   XoX##############XX          
   XoX####%%###XXXXX%%          
   XXX####%%%XXXXX&%%%          
   X$XXXXXX%%%*===%%%           
    XXXXXX-;%%%::%%%&&          
         &>>>%%%%%%>>>&         
  &&&&&&&&,,,,%%%%,,,,&&&&&&&&  
 &<<<<<<<&1111%%%%1111&<<<<<<<& 
 &<<<<<<<&222%%%%%%222&<<<<<<<& 
  &&&&&&&&33%%%33%%%33&&&&&&&&  
         &4%%%4444%%%4&         
          %%%555555%%%          
          %%        %%          '''
load_xpm = '''32 32 6 1
  c None
. c #00FF00
O c #8000FF
o c #8080FF
+ c #FF0000
X c #C0C0C0
                  ..            
                ......          
               ........         
               .........        
              ...... ....       
              .....   ....      
             .....      ..      
             .....              
        ..   .....   ..         
        ...  .....  ...         
         ... ..... ...          
          ...........           
    XXXXXXX.........XXXXXXXX    
   XXooooooo.......ooooooooXX   
  XXooooooooo.....ooooooooooXX  
 XXooooooooooo...ooooooooooooXX 
 Xooooooooooooo.ooooooooooooooXO
 XooooooooooooooooooooooooooooXO
 XXooooooooooooooooooooooooooXXO
  XXooooooooooooooooooooooooXXOO
  OXXooooooooooooooooooooooXXOOO
  OOXXXXXXXXXXXXXXXXXXXXXXXXOOO 
   OOOOOOOOOOOOOOOOOOOOOOOOOOO  
    OO+++OOOOOOOOOOOOOOOOOOOO   
     OOOOOOOOOOOOOOOOOOOOOOO    
                                
                                
                                
                                
                                
                                
                                '''
send_xpm = '''32 32 6 1
  c None
. c #00FF00
O c #8000FF
o c #FFFF00
+ c #FF0000
X c #C0C0C0
                        ...     
                         ...    
                          ...   
                      ........  
                   ............ 
                 ...............
                ............... 
               ...............  
               ....       ...   
              ....       ...    
              ...       ...     
              ..                
    XXXXXXXXXX.XXXXXXXXXXXXX    
   XXooooooooooooooooooooooXX   
  XXooooooooooooooooooooooooXX  
 XXooooooooooooooooooooooooooXX 
 XooooooooooooooooooooooooooooXO
 XooooooooooooooooooooooooooooXO
 XXooooooooooooooooooooooooooXXO
  XXooooooooooooooooooooooooXXOO
  OXXooooooooooooooooooooooXXOOO
  OOXXXXXXXXXXXXXXXXXXXXXXXXOOO 
   OOOOOOOOOOOOOOOOOOOOOOOOOOO  
    OO+++OOOOOOOOOOOOOOOOOOOO   
     OOOOOOOOOOOOOOOOOOOOOOO    
                                
                                
                                
                                
                                
                                
                                '''
remote_delete_xpm = '''32 32 6 1
  c None
X c #8000FF
+ c #000080
. c #FF0000
o c #FFFF80
O c #00FF00
                       .        
         ...          .X.       
       ..XXX...     ..XoX.      
     ..XXoooXXX..  .XXoOoX..    
   ..XXooooooooXX..XooOOooXX.   
  .XXooooooooooOOXXoooOoooooX.  
  .XoOOooooooOOOoooooOOooooooX. 
  .XooOOoooooooooooooOooooOOOoX.
  .XoooOoo++++++++oooOooOOOooX. 
 .XooooOOo+++++++++oooOOOooooX. 
 .XoooooOo+++oooo+++oOOoooooX.  
 .XoooooOo++oooooo++oooooooX.   
 .XoooooOo++oooooo++ooooooX.    
.XoOOooooo+++oooo+++ooooooX.    
.XooOOOooo+++++++++oooOOOX.     
.XooooOOOo++++++++oooOOoooX.    
.XooooooOo+++ooooooOOOooooX.    
 .XoooooOo++++ooooOOoooooooX.   
 .Xooooooo+++++oooooooooooooX.  
 .XooooOOo++o+++oooOOOOOOOooX.  
 .XoooOOoo++oo+++ooooooooOOOoX. 
  .XooOooo++ooo+++ooOOOoooooX.  
  .XoOOooo++oooo+++oooOOooooX.  
  .XoOoooo++ooooo+++oooOoooX.   
 .XoOOoooo++oooooo+++ooOooX.    
 .XoooooOo++ooooooo++ooOooX.    
 .XoooooOoooooooooooooOooX.     
.XooooooOOooooooooooooOoX.      
.XXooooooOOooXXXXXXXXXooX.      
...XXXXoooOoX.........XX.       
   ....XXXoX.         ..        
       ...XX.                   '''

UpdateStatusBarEvent, EVT_UPDATE_STATUS_BAR = NewEvent()
UpdateGridCellEvent, EVT_UPDATE_GRID_CELL = NewEvent()
EventTreeListSetCellValue, EVT_TREE_LIST_SET_CELL_VALUE = NewEvent()
EventTreeListSetItemImage, EVT_TREE_LIST_SET_ITEM_IMAGE = NewEvent()
EventTreeListSetItemData, EVT_TREE_LIST_SET_ITEM_DATA = NewEvent()
ToolBarEvent, EVT_TOOL_BAR = NewEvent()
ConnectTrobberEvent, EVT_CONNECT_TROBBER = NewEvent()
SearchTrobberEvent, EVT_SEARCH_TROBBER = NewEvent()

def print_error():
	exc, err, traceback = sys.exc_info()
	print exc, traceback.tb_frame.f_code.co_filename, 'ERROR ON LINE', traceback.tb_lineno, '\n', err
	del exc, err, traceback

def open_settings(filename):
	conf = wx.FileConfig(localFilename = filename)
	def create_entry(entry_name, entry_value):
		if not conf.HasEntry(entry_name):
			if isinstance(entry_value, (str, unicode)):
				conf.Write(entry_name, entry_value)
			elif isinstance(entry_value, int):
				conf.WriteInt(entry_name, entry_value)
			elif isinstance(entry_value, bool):
				conf.WriteBool(entry_name, entry_value)
			else:
				conf.Write(entry_name, repr(entry_value))
			return True
		else:
			return False
	flag_flush = False
	if create_entry('Language/Catalog', getdefaultlocale()[0]):
		flag_flush = True
	if create_entry('GUI/load_default_perspective_on_start', True):
		flag_flush = True
	if create_entry('GUI/save_default_perspective_on_exit', True):
		flag_flush = True
	if create_entry('GUI/perspective', ''):
		flag_flush = True
	if create_entry('GUI/load_default_state_on_start', True):
		flag_flush = True
	if create_entry('GUI/save_default_state_on_exit', True):
		flag_flush = True
	if create_entry('GUI/fullscreen_style', default_fullscreen_style):
		flag_flush = True
	if create_entry('GUI/centre_on_screen', repr((False, wx.BOTH))):
		flag_flush = True
	if create_entry('GUI/default_open_path', ''):
		flag_flush = True
	if create_entry('Connect/server_host', '127.0.0.1'):
		flag_flush = True
	if create_entry('Connect/server_port', 18812):
		flag_flush = True
	if create_entry('Connect/server_root', '/'):
		flag_flush = True
	if create_entry('Connect/packet_size', 5242880):
		flag_flush = True
	if flag_flush:
		conf.Flush()
	return conf

def int_to_str(value_int, sep = ' ', width = 3):
	value_str = str(value_int)
	len_str = len(value_str)
	if len_str > width:
		loops = len(value_str) / width
		temp_str = value_str
		a = len_str
		value_str = temp_str[a-width:a]
		for x in range(loops):
			a -= width
			start = a-width
			if start < 0:
				value_str = (temp_str[0:a] + sep + value_str).lstrip()
			else:
				value_str = temp_str[start:a] + sep + value_str
	return value_str

def create_root_path(prefix = 'c:', suffix = ''):
	result = prefix + suffix
	if os.name in ('posix', ):
		result = '/.'
	return result

def create_full_path(path, name):
	if path.endswith('\\') or path.endswith('/'):
		return path + name
	else:
		return path + '/' + name

def create_bmp_from_xpm(str_xpm_data, size = None, repl = None):
	list_xpm_data = str_xpm_data.split('\n')
	if repl is not None:
		for item in repl:
			list_xpm_data[item[0]] = item[1]
	if size is None:
		return wx.BitmapFromXPMData(list_xpm_data)
	else:
		img = wx.BitmapFromXPMData(list_xpm_data).ConvertToImage()
		img.Rescale(size[0], size[1])
		return img.ConvertToBitmap()

def create_client_socket(server = '127.0.0.1', port = 18812):
	from Rpyc import SocketConnection
	sock = SocketConnection(server, port)
	return sock

def create_remote_functions(conn):
	body_remote_funcs = '''
from os import listdir, walk, remove, rmdir, mkdir, makedirs
from os.path import isdir, isfile, getsize, exists, join
def open_file(file_name, flags = 'wrb'): return file(file_name, flags)
def read_to_buf(file_descriptor, pos, size):
	file_descriptor.seek(pos)
	buf = file_descriptor.read(size)
	return buf
def read_only_to_buf(file_descriptor, size):
	return file_descriptor.read(size)
def write_buf_to_file(file_descriptor, buf, pos):
	file_descriptor.write(buf)
	file_descriptor.seek(pos)
def close_file(file_descriptor): file_descriptor.close()
def path_exists(path): return exists(path)
def is_dir(path): return isdir(path)
def create_path(path, mode = 0777):
	try: mkdir(path, mode)
	except: return False
	else: return True
def create_full_path(path, mode = 0777):
	try: makedirs(path, mode)
	except: return False
	else: return True
def delete_path(path):
	if isdir(path):
		for root, dirs, files in walk(path, topdown=False):
			for name in files: remove(join(root, name))
			for name in dirs: rmdir(join(root, name))
		rmdir(path)
	else: remove(path)
def list_dir(folder_name):
	list_dir_with_info = []
	try: list_dir = listdir(folder_name)
	except: pass
	else:
		for item in list_dir:
			full_path = folder_name + item
			size = 0
			try: size = getsize(full_path)
			except: pass
			list_dir_with_info.append((isdir(full_path), item, size, folder_name))
		list_dir_with_info.sort(reverse = True)
	return list_dir_with_info
def remote_getsize(path): return getsize(path)
def remote_walk(path): return walk(path)
'''
	conn.execute(body_remote_funcs)

def add_result_row(rlist, name_item, root_path, size = 0, is_dir = True):
	len_data = len(rlist.data)
	rlist.data.append((str(len_data), name_item, root_path, int_to_str(size), is_dir))
	rlist.SetItemCount(len_data)

def search_file_system_item(frame, path, pattern = '\.py$'):
	ns = frame.connection.namespace
	if isinstance(path, unicode): path = path.encode(gui_codec)
	if isinstance(pattern, unicode): pattern = pattern.encode(gui_codec)
	if ns.path_exists(path):
		remote_tree = ns.remote_walk(path)
		re_obj = re.compile(pattern)
		for root, dirs, files in remote_tree:
			if re_obj.search(root) is not None:
				add_result_row(frame.search_panel.search_result, root, path)
			for name in dirs:
				if re_obj.search(name) is not None:
					add_result_row(frame.search_panel.search_result, name, root)
			for name in files:
				if re_obj.search(name) is not None:
					add_result_row(frame.search_panel.search_result, name, root, ns.remote_getsize(root + '/' + name), False)
			if frame.search_panel.not_stop_search_process: break
		frame.aui_manager.Update()
	#frame.cancel_remote_find()

def load_file(frame, grid_row, src_file_name, dst_file_name, file_size = 0, packet_size = 1048576):
	write_file_flags = None
	if os.path.isfile(dst_file_name):
		if os.path.getsize(dst_file_name) < file_size:
			result = wx.MessageBox(_('Continue write to exists file ("Yes" button)\nor create new file ("No" button)?\nElse cancel operation.'), _('Warning'), wx.YES_NO | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION)
			if result == wx.YES:
				write_file_flags = 'ab'
			elif result == wx.NO:
				write_file_flags = 'wb'
		else:
			if wx.MessageBox(_('Rewrite existing file?'), _('Warning'), wx.OK | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION) == wx.OK:
				write_file_flags = 'wb'
	else:
		write_file_flags = 'wb'
	if write_file_flags is not None:
		ns = frame.connection.namespace
		if ns.path_exists(src_file_name):
			read_file = ns.open_file(src_file_name, 'rb')
			pos = 0
			if write_file_flags == 'ab':
				pos = os.path.getsize(dst_file_name)
			buf = ns.read_to_buf(read_file, pos, packet_size)
			buf_len = pos + len(buf)
			if buf is not None:
				write_file = file(dst_file_name, write_file_flags)
				while buf:
					wx.PostEvent(frame.task_panel, UpdateGridCellEvent(row = grid_row, col = 3, value = int_to_str(buf_len)))
					write_file.write(buf)
					pos += packet_size
					write_file.seek(pos)
					#~ buf = ns.read_to_buf(read_file, pos, packet_size)
					buf = ns.read_only_to_buf(read_file, packet_size)
					buf_len += len(buf)
				write_file.close()
			ns.close_file(read_file)
			wx.PostEvent(frame.task_panel, UpdateGridCellEvent(row = grid_row, col = 0, value = '1'))
			del buf
		else:
			wx.PostEvent(frame.task_panel, UpdateStatusBarEvent(status_text = _('Not exists path') + ' ' + src_file_name))
	else:
		wx.PostEvent(frame.task_panel, UpdateStatusBarEvent(status_text = _('Canceled operation with path') + ' ' + src_file_name))

def send_file(frame, grid_row, src_file_name, dst_file_name, file_size = 0, packet_size = 1048576):
	if os.path.exists(src_file_name):
		ns = frame.connection.namespace
		write_file_flags = None
		if ns.isfile(dst_file_name):
			if ns.getsize(dst_file_name) < file_size:
				result = wx.MessageBox(_('Continue write to exists file ("Yes" button)\nor create new file ("No" button)?\nElse cancel operation.'), _('Warning'), wx.YES_NO | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION)
				if result == wx.YES:
					write_file_flags = 'ab'
				elif result == wx.NO:
					write_file_flags = 'wb'
			else:
				if wx.MessageBox(_('Rewrite existing file?'), _('Warning'), wx.OK | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION) == wx.OK:
					write_file_flags = 'wb'
		else:
			write_file_flags = 'wb'
		if write_file_flags is not None:
			read_file = file(src_file_name, 'rb')
			pos = 0
			if write_file_flags == 'ab':
				pos = ns.getsize(dst_file_name)
				if pos > 0:
					read_file.seek(pos)
			buf = read_file.read(packet_size)
			buf_len = pos + len(buf)
			if buf is not None:
				write_file = ns.open_file(dst_file_name, write_file_flags)
				while buf:
					wx.PostEvent(frame.task_panel, UpdateGridCellEvent(row = grid_row, col = 3, value = int_to_str(buf_len)))
					pos += packet_size
					ns.write_buf_to_file(write_file, buf, pos)
					read_file.seek(pos)
					buf = read_file.read(packet_size)
					buf_len += len(buf)
				ns.close_file(write_file)
			read_file.close()
			del buf
			wx.PostEvent(frame.task_panel, UpdateGridCellEvent(row = grid_row, col = 0, value = '3'))
		else:
			wx.PostEvent(frame.task_panel, UpdateStatusBarEvent(status_text = _('Not exists path') + ' ' + src_file_name))
	else:
		wx.PostEvent(frame.task_panel, UpdateStatusBarEvent(status_text = _('Not exists path') + ' ' + src_file_name))

def load_file_to_dir(tree, item, data, size):
	src = data['full_path']
	local_path = data['destination']
	dst = create_full_path(local_path, data['name'])
	ns = tree.parent.connection.namespace
	if ns.path_exists(src):
		local_path_exists = True
		if not os.path.exists(local_path):
			try:
				os.makedirs(local_path)
			except:
				local_path_exists = False
				print_error()
			else:
				local_path_exists = True
		if local_path_exists:
			pos = 0
			read_file = ns.open_file(src, 'rb')
			buf = ns.read_to_buf(read_file, pos, size)
			buf_len = len(buf)
			if buf is not None:
				write_file = file(dst, 'wb')
				while buf:
					wx.PostEvent(tree, EventTreeListSetCellValue(item = item, col = 2, value = int_to_str(buf_len)))
					pos += size
					ns.write_buf_to_file(write_file, buf, pos)
					read_file.seek(pos)
					buf = ns.read_to_buf(read_file, pos, size)
					buf_len += len(buf)
				write_file.close()
			ns.close_file(read_file)
			del buf
			data['complete'] = True
			wx.PostEvent(tree, EventTreeListSetItemData(item = item, data = data))
			wx.PostEvent(tree, EventTreeListSetItemImage(item = item, images = ((1, wx.TreeItemIcon_Normal), )))
	else: wx.PostEvent(tree.parent, UpdateStatusBarEvent(status_text = _('Not exists path') + ' ' + src))

def recursion_load_file(tree, task_tree_item, size = 1048576):
	child, cookie = tree.GetFirstChild(task_tree_item)
	while child.IsOk():
		task = tree.GetPyData(child)
		if not task['complete'] and task['isdir']:
			recursion_load_file(tree, child, size)
		else:
			load_file_to_dir(tree, child, task, size)
		child, cookie = tree.GetNextChild(task_tree_item, cookie)
	data = tree.GetPyData(task_tree_item)
	data['complete'] = True
	wx.PostEvent(tree, EventTreeListSetItemData(item = task_tree_item, data = data))
	wx.PostEvent(tree, EventTreeListSetItemImage(item = task_tree_item, images = ((6, wx.TreeItemIcon_Normal), (7, wx.TreeItemIcon_Expanded))))

def send_file_from_dir(tree, item, data, size):
	src = data['full_path']
	remote_path = data['destination']
	dst = create_full_path(remote_path, data['name'])
	if os.path.exists(src):
		ns = tree.parent.connection.namespace
		remote_path_exists = True
		if not ns.path_exists(remote_path):
			remote_path_exists = ns.create_full_path(remote_path)
		if remote_path_exists:
			pos = 0
			read_file = file(src, 'rb')
			buf = read_file.read(size)
			buf_len = len(buf)
			if buf is not None:
				write_file = ns.open_file(dst, 'wb')
				while buf:
					wx.PostEvent(tree, EventTreeListSetCellValue(item = item, col = 2, value = int_to_str(buf_len)))
					pos += size
					ns.write_buf_to_file(write_file, buf, pos)
					read_file.seek(pos)
					buf = read_file.read(size)
					buf_len += len(buf)
				ns.close_file(write_file)
			read_file.close()
			del buf
			data['complete'] = True
			wx.PostEvent(tree, EventTreeListSetItemData(item = item, data = data))
			wx.PostEvent(tree, EventTreeListSetItemImage(item = item, images = ((3, wx.TreeItemIcon_Normal), )))
	else:
		wx.PostEvent(tree.parent, UpdateStatusBarEvent(status_text = _('Not exists path') + ' ' + src))

def recursion_send_file(tree, task_tree_item, size = 1048576):
	child, cookie = tree.GetFirstChild(task_tree_item)
	while child.IsOk():
		task = tree.GetPyData(child)
		if not task['complete'] and task['isdir']:
			recursion_send_file(tree, child, size)
		else:
			send_file_from_dir(tree, child, task, size)
		child, cookie = tree.GetNextChild(task_tree_item, cookie)
	data = tree.GetPyData(task_tree_item)
	data['complete'] = True
	wx.PostEvent(tree, EventTreeListSetItemData(item = task_tree_item, data = data))
	wx.PostEvent(tree, EventTreeListSetItemImage(item = task_tree_item, images = ((10, wx.TreeItemIcon_Normal), (11, wx.TreeItemIcon_Expanded))))

def delete_path(conn, path):
	conn.namespace.delete_path(path)

def query_list_dir(conn, path):
	return conn.namespace.list_dir(path)

def recursion_fill_tree_dir(tree, path, root):
	remote_list = tree.parent.connection.namespace.list_dir(path)
	for item in remote_list:
		if tree.parent.flag_fill_tree:
			tree_item = tree.AppendItem(root, item[1])
			tree.SetItemText(tree_item, int_to_str(item[2]), 1)
			tree.SetItemText(tree_item, item[3], 2)
			tree.SetItemImage(tree_item, 1, which = wx.TreeItemIcon_Expanded)
			tree.items.append(tree_item)
			if item[0]:
				tree.SetItemImage(tree_item, 0, which = wx.TreeItemIcon_Normal)
				recursion_fill_tree_dir(tree, item[3]+item[1]+'/', tree_item)
			else:
				tree.SetItemImage(tree_item, 2, which = wx.TreeItemIcon_Normal)

def threaded_fill_tree_dir(tree, path, root):
	recursion_fill_tree_dir(tree, path, root)
	tree.Expand(tree.root)
	#~ wx.PostEvent(tree.parent,
		#~ ToolBarEvent(
			#~ toolbar = tree.parent.main_toolbar,
			#~ delete_tool_id = tree.parent.id_cancel_fill_tree,
			#~ insert_pos = 0,
			#~ insert_tool_id = tree.parent.id_connect,
			#~ insert_caption = _('Connect'),
			#~ insert_bitmap1 = tree.parent.bmp_net_dir,
			#~ insert_bitmap2 = wx.NullBitmap,
			#~ insert_tool_state = wx.ITEM_NORMAL,
			#~ insert_desc1 = _('Connect to remote host'),
			#~ insert_desc2 = _('Connect to remote host')
			#~ ))
	wx.PostEvent(tree.parent.conn_panel, ConnectTrobberEvent(start = False))

def remote_isdir(conn, path):
	return conn.namespace.is_dir(path)

def remote_path_exists(conn, path):
	return conn.namespace.path_exists(path)

def start_rpyc_server():
	from Rpyc.Utils.Serving import DEFAULT_PORT, threaded_server, start_discovery_agent_thread
	start_discovery_agent_thread(rpyc_port = DEFAULT_PORT)
	threaded_server(port = DEFAULT_PORT)

class py_drop_target(wx.PyDropTarget):
	def __init__(self, mf):
		wx.PyDropTarget.__init__(self)
		self.mf = mf
		self.data_object = wx.CustomDataObject('remote_tree_data_object')
		self.SetDataObject(self.data_object)

	def OnEnter(self, x, y, d):
		return wx.DragCopy

	def OnDragOver(self, x, y, d):
		return wx.DragCopy

##	def OnLeave(self):
##		print "OnLeave\n"

	def OnDrop(self, x, y):
		return True

	def OnData(self, x, y, d):
		if self.GetData():
			data = cPickle.loads(self.data_object.GetData())
			self.mf.sb.SetStatusText(data[1])
			if isinstance(data[1], (str, unicode)):
				if len(data[1]) > 0:
					if remote_isdir(self.mf.connection, create_full_path(data[0], data[1])):
						self.mf.task_tree_panel.add_load_dir(data[0], data[1], create_full_path(data[0], data[1]), self.mf.local_tree.GetPath())
					else:
						self.mf.task_panel.add_task_load(data[0], data[1], self.mf.local_tree.GetPath(), data[2])
		return d

class text_drop_target(wx.TextDropTarget):
	def __init__(self, mf):
		wx.TextDropTarget.__init__(self)
		self.mf = mf
	def OnDropText(self, x, y, text):
		if self.mf.connection == None:
			self.mf.sb.SetStatusText(_('Connection closed.') + text)
		else:
			self.mf.sb.SetStatusText(text)

class file_drop_target(wx.FileDropTarget):
	def __init__(self, mf):
		wx.FileDropTarget.__init__(self)
		self.mf = mf
	def OnDropFiles(self, x, y, filenames):
		if self.mf.connection == None:
			self.mf.sb.SetStatusText(_('Connection closed.'))
		else:
			item = self.mf.remote_tree.GetSelection()
			if item.IsOk():
				is_ok = True
				remote_item = self.mf.remote_tree.GetItemText(item, 0)
				remote_root = self.mf.remote_tree.GetItemText(item, 2)
				remote_path = remote_root + remote_item
				if not remote_isdir(self.mf.connection, remote_path):
					item = self.mf.remote_tree.GetItemParent(item)
					if item.IsOk():
						remote_item = self.mf.remote_tree.GetItemText(item, 0)
						remote_root = self.mf.remote_tree.GetItemText(item, 2)
						remote_path = remote_root + remote_item
					else: is_ok = False
				if is_ok:
					from os.path import realpath, basename, dirname
					for file in filenames:
						#if isinstance(file, unicode): file = file.encode(gui_codec)
						if os.path.isdir(file):
							self.mf.task_tree_panel.add_send_dir(dirname(file), basename(file), realpath(file), remote_path)
						else:
							self.mf.task_panel.add_task_send(dirname(file), basename(file), remote_path, os.path.getsize(realpath(file)))

class bitmap_renderer(gr.PyGridCellRenderer):
	def __init__(self, bitmaps):
		gr.PyGridCellRenderer.__init__(self)
		self.bitmaps = bitmaps
	def Draw(self, grid, attr, dc, rect, row, col, isSelected):
		value = grid.GetCellValue(row, col)
		bmp = self.bitmaps[int(value)]
		w, h = bmp.GetWidth(), bmp.GetHeight()
		image = wx.MemoryDC()
		image.SelectObject(bmp)
		dc.SetBackgroundMode(wx.SOLID)
		if isSelected: dc.SetBrush(wx.Brush(wx.Colour(200, 100, 255), wx.SOLID))
		else: dc.SetBrush(wx.Brush(wx.Colour(215, 240, 230), wx.SOLID))
		dc.DrawRectangleRect(rect)
		dc.Blit(rect.x + rect.width/2 - w/2, rect.y + rect.height/2 - h/2, w, h, image, 0, 0, wx.COPY, True)
	def Clone(self): return bitmap_renderer(self.bitmaps)

class remote_tree_ctrl(TreeListCtrl):
	def __init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT):
		TreeListCtrl.__init__(self, parent, id, pos, size, style)
		self.parent = parent

		isz = (16,16)
		self.il = wx.ImageList(isz[0], isz[1])
		self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
		self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
		self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
		self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_OTHER, isz))
		self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_WARNING, wx.ART_OTHER, isz))
		self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_TIP, wx.ART_OTHER, isz))
		self.SetImageList(self.il)

		self.AddColumn(_('Name'))
		self.AddColumn(_('Size'))
		self.AddColumn(_('Root'))
		self.SetMainColumn(0)
		self.SetColumnWidth(0, 200)
		self.SetColumnWidth(1, 100)
		self.SetColumnWidth(2, 200)
		self.create_root()

		self.GetMainWindow().Bind(wx.EVT_LEFT_UP, self.event_left_up)
		#self.GetMainWindow().Bind(wx.EVT_LEFT_DOWN, self.event_left_down)
		self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.event_tree_begin_drag)

	def create_root(self, remote_dir = '........', caption = _('List Remote Files')):
		self.root = self.AddRoot(remote_dir)
		self.SetItemText(self.root, caption, 1)
		self.SetItemImage(self.root, 0, which = wx.TreeItemIcon_Normal)
		self.SetItemImage(self.root, 1, which = wx.TreeItemIcon_Expanded)
		self.items = [self.root]

	#~ def add_remote_list(self, remote_list, remote_dir = '........', caption = _('List Remote Files')):
		#~ self.parent.conn_panel.throb.Start()
		#~ if len(remote_list) > 0:
			#~ self.DeleteAllItems()
			#~ self.create_root(remote_dir, caption)
			#~ for item in remote_list:
				#~ is_dir = item[0]
				#~ name = item[1]
				#~ size = str(item[2])
				#~ path = item[1]
				#~ if not isinstance(name, unicode) and wx.USE_UNICODE: name = name.decode(gui_codec)
				#~ else: name = name.encode(gui_codec)
				#~ if not isinstance(path, unicode) and wx.USE_UNICODE: path = path.decode(gui_codec)
				#~ else: path = path.encode(gui_codec)
				#~ it = self.AppendItem(self.root, name)
				#~ self.SetItemText(it, size, 1)
				#~ self.SetItemText(it, path, 2)
				#~ if is_dir: self.SetItemImage(it, 0, which = wx.TreeItemIcon_Normal)
				#~ else: self.SetItemImage(it, 2, which = wx.TreeItemIcon_Normal)
				#~ self.SetItemImage(it, 1, which = wx.TreeItemIcon_Expanded)
				#~ self.items.append(it)
			#~ self.Expand(self.root)
		#~ self.parent.conn_panel.throb.Stop()

	def add_remote_tree(self, remote_dir = '........', caption = _('List Remote Files')):
		self.parent.conn_panel.throb.Start()
		self.DeleteAllItems()
		self.create_root(remote_dir, caption)
		t = Thread(target = threaded_fill_tree_dir, args = (self, remote_dir, self.root))
		t.setDaemon(True)
		t.start()

	def clear(self):
		self.DeleteAllItems()
		self.create_root()

	def event_left_up(self, event):
		if self.parent.connection == None:
			self.parent.sb.SetStatusText(_('Connection closed.'))
		else:
			local_folder = self.parent.local_tree.GetPath()
			if local_folder == '' or not os.path.isdir(local_folder):
				self.parent.sb.SetStatusText(_('Not selected local folder!!!'))
			else:
				pt = event.GetPosition()
				remote_item, flags, col = self.HitTest(pt)
				if remote_item.IsOk():
					if self.GetItemText(remote_item, 0) != self.GetItemText(self.root, 0):
						remote_item_name = self.GetItemText(remote_item, 0)
						remote_root = self.GetItemText(remote_item, 2)
						self.parent.task_panel.add_task_load(remote_root, remote_item_name, local_folder, self.GetItemText(remote_item, 1))
					else:
						self.parent.sb.SetStatusText(_('Not select root item.'))
				else:
					self.parent.sb.SetStatusText(_('Not selected remote item.'))

	def event_left_down(self, event):
		remote_item, flags, col = self.HitTest(event.GetPosition())
		self.drag_operation(remote_item)

	def event_tree_begin_drag(self, event):
		self.drag_operation(event.GetItem())

	def drag_operation(self, remote_item):
		if self.parent.connection == None:
			self.parent.sb.SetStatusText(_('Connection closed.'))
		else:
			local_folder = self.parent.local_tree.GetPath()
			if local_folder == '' or not os.path.isdir(local_folder):
				self.parent.sb.SetStatusText(_('Not selected local folder!!!'))
			else:
				self.parent.sb.SetStatusText('')
				if remote_item.IsOk():
					if self.GetItemText(remote_item, 0) != self.GetItemText(self.root, 0):
						remote_item_name = self.GetItemText(remote_item, 0)
						remote_root = self.GetItemText(remote_item, 2)
						remote_size = self.GetItemText(remote_item, 1)
						data = wx.CustomDataObject('remote_tree_data_object')
						data.SetData(cPickle.dumps([remote_root, remote_item_name, remote_size]))
						drop_source = wx.DropSource(self)
						drop_source.SetData(data)
						result = drop_source.DoDragDrop(wx.Drag_CopyOnly)
						#~ if result == wx.DragCopy:
							#~ self.Refresh()

class connect_panel(ScrolledPanel):
	def __init__(self, parent):
		self.app = parent.app
		ScrolledPanel.__init__(self, parent, wx.ID_ANY, style = wx.TAB_TRAVERSAL)

		sizer = RowColSizer()

		sizer.Add(wx.StaticText(self, wx.ID_ANY, _('host')), row=0, col=0, flag=wx.ALIGN_BOTTOM)
		self.txt_host = wx.TextCtrl(self, wx.ID_ANY, self.app.settings.Read('Connect/server_host', '127.0.0.1'))
		sizer.Add(self.txt_host, row=1, col=0)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, _('port')), row=0, col=2, flag=wx.ALIGN_BOTTOM)
		self.txt_port = wx.TextCtrl(self, wx.ID_ANY, str(self.app.settings.ReadInt('Connect/server_port', 18812)))
		sizer.Add(self.txt_port, row=1, col=2)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, _('remote root')), row=0, col=4, flag=wx.ALIGN_BOTTOM)
		self.txt_remote_root = wx.TextCtrl(self, wx.ID_ANY, self.app.settings.Read('Connect/server_root', create_root_path()))
		sizer.Add(self.txt_remote_root, row=1, col=4)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, _('packet size (bytes)')), row=0, col=6, flag=wx.ALIGN_BOTTOM)
		self.txt_packet_size = wx.TextCtrl(self, wx.ID_ANY, str(self.app.settings.ReadInt('Connect/packet_size', 5242880)))
		sizer.Add(self.txt_packet_size, row=1, col=6)

		img_size = (16, 16)
		throbber_images = []
		for a in range(8):
			repl = [(i + 3, '%d c #8080C0'%i) for i in range(8) if i is not a]
			repl.append((a + 3, '%d c #00FF00'%a))
			throbber_images.append(create_bmp_from_xpm(throbber_xpm, repl = repl))
		self.throb = Throbber(self, wx.ID_ANY, throbber_images, size = img_size, frameDelay = 0.1)
		sizer.Add(self.throb, row=1, col=9)

		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		self.SetupScrolling()

		EVT_CONNECT_TROBBER(self, self.event_trobber)

	def event_trobber(self, event):
		if event.start:
			self.throb.Start()
		else:
			self.throb.Stop()

class result_search(wx.ListCtrl):
	def __init__(self, parent, bitmaps):
		wx.ListCtrl.__init__(self, parent, wx.ID_ANY, size = (600, 400), style = wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
		self.data = []
		self.il = wx.ImageList(16, 16)
		self.idx0 = self.il.Add(bitmaps[0])
		self.idx1 = self.il.Add(bitmaps[1])
		self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
		self.InsertColumn(0, '...')
		self.InsertColumn(1, _('Name item'))
		self.InsertColumn(2, _('Path'))
		self.InsertColumn(3, _('Size'))
		self.SetColumnWidth(0, 50)
		self.SetColumnWidth(1, 150)
		self.SetColumnWidth(2, 300)
		self.SetColumnWidth(3, 100)
		self.attr = wx.ListItemAttr()
		self.attr.SetBackgroundColour('light blue')
	def getColumnText(self, index, col):
		item = self.GetItem(index, col)
		return item.GetText()
	def OnGetItemText(self, item, col): return self.data[item][col]
	def OnGetItemImage(self, item):
		if self.data[item][4]: return self.idx0
		else: return self.idx1
	def OnGetItemAttr(self, item):
		if self.data[item][4]: return self.attr
		else: return None

class search_panel(ScrolledPanel):
	def __init__(self, parent):
		ScrolledPanel.__init__(self, parent, wx.ID_ANY, style = wx.TAB_TRAVERSAL)
		self.parent = parent
		self.not_stop_search_process = False

		img_size = (16, 16)
		bmp_dir = wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, img_size)
		bmp_file = wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, img_size)

		sizer = RowColSizer()

		self.search_ctrl = wx.SearchCtrl(self, value = '\.py$', style = wx.TE_PROCESS_ENTER)
		sizer.Add(self.search_ctrl, row=0, col=0, colspan=4)

		throbber_images = []
		for a in range(8):
			repl = [(i + 3, '%d c #00FF00'%i) for i in range(8) if i is not a]
			repl.append((a + 3, '%d c #8080C0'%a))
			throbber_images.append(create_bmp_from_xpm(throbber_xpm, repl = repl))
		self.throb = Throbber(self, wx.ID_ANY, throbber_images, size = img_size, frameDelay = 0.1)
		sizer.Add(self.throb, row=0, col=4)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, _('path')), row=0, col=5)
		self.root_path = wx.TextCtrl(self, wx.ID_ANY, create_root_path(suffix = '/'))
		sizer.Add(self.root_path, row=0, col=6, colspan=10)

		self.search_result = result_search(self, (bmp_dir, bmp_file))
		sizer.Add(self.search_result, row=1, col=0, colspan=16, rowspan=4)

		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		self.SetupScrolling()

		self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search_ctrl)
		self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel, self.search_ctrl)
		self.search_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search_ctrl)

	def OnSearch(self, evt): self.parent.remote_find()
	def OnCancel(self, evt): self.parent.cancel_remote_find()
	def OnDoSearch(self, evt): self.parent.remote_find()

class task_grid(gr.Grid):
	def __init__(self, parent, bitmaps):
		gr.Grid.__init__(self, parent, wx.ID_ANY)
		self.parent = parent
		self.CreateGrid(0, 5)

		self.SetColSize(0, 16)
		self.SetColLabelValue(0, '...')
		self.SetColFormatNumber(0)

		self.SetColSize(1, 200)
		self.SetColLabelValue(1, _('Source'))

		self.SetColSize(2, 200)
		self.SetColLabelValue(2, _('Destination'))

		self.SetColSize(3, 100)
		self.SetColLabelValue(3, _('Indicator')) 

		self.SetColSize(4, 100)
		self.SetColLabelValue(4, _('Size')) 

		self.SetColLabelSize(20)
		self.SetRowLabelSize(30)
		self.SetSelectionMode(gr.Grid.wxGridSelectRows)

		attr = gr.GridCellAttr()
		attr.SetRenderer(bitmap_renderer(bitmaps))
		attr.SetReadOnly()
		self.SetColAttr(0, attr)

		attr_read_only = gr.GridCellAttr()
		attr_read_only.SetReadOnly()
		self.SetColAttr(1, attr_read_only)
		self.SetColAttr(3, attr_read_only)
		self.SetColAttr(4, attr_read_only)

		EVT_UPDATE_GRID_CELL(self, self.event_update_grid_cell)

	def event_update_grid_cell(self, event):
		self.SetCellValue(event.row, event.col, event.value)

	def add_task(self, source, item, destination_path, size, load_send = '0'):
		destination = create_full_path(destination_path, item)
		txt = 'load'
		if load_send is not '0':
			txt = 'send'
		self.parent.sb.SetStatusText(source + _(' --> ' + txt + ' to --> ') + destination)
		self.parent.task_panel.AppendRows()
		last_row = self.GetNumberRows() - 1
		self.parent.task_panel.SetCellValue(last_row, 0, load_send)
		self.parent.task_panel.SetCellValue(last_row, 1, source)
		self.parent.task_panel.SetCellValue(last_row, 2, destination)
		if isinstance(size, (int, long)):
			size = int_to_str(size)
		self.parent.task_panel.SetCellValue(last_row, 4, size)

	def add_task_load(self, path, item, destination_path, size):
		source = create_full_path(path, item)
		if remote_isdir(self.parent.connection, source):
			self.parent.sb.SetStatusText(_('Remote item must be file!!!'))
		else:
			self.add_task(source, item, destination_path, size)

	def add_task_send(self, path, item, destination_path, size):
		source = create_full_path(path, item)
		if os.path.isdir(source):
			self.parent.sb.SetStatusText(_('Local item must be file!!!'))
		else:
			self.add_task(source, item, destination_path, size, '2')

class task_tree(TreeListCtrl):
	'''
	bitmaps:
	0	load file
	1	loaded file
	2	send file
	3	sended file
	4	load dir
	5	load dir expanded
	6	loaded dir
	7	loaded dir expanded
	8	send dir
	9	send dir expanded
	10	sended dir
	11	sended dir expanded
	'''
	def __init__(self, *args, **kwargs):
		kwargs['style'] = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT
		images = kwargs.pop('images')
		super(task_tree, self).__init__(*args, **kwargs)
		self.parent = args[0]
		self.il = wx.ImageList(16, 16)
		for bmp in images: self.il.Add(bmp)
		self.SetImageList(self.il)
		self.AddColumn(_('Source'))
		self.AddColumn(_('Destination'))
		self.AddColumn(_('Indicator'))
		self.AddColumn(_('Size'))
		self.SetMainColumn(0)
		self.SetColumnWidth(0, 200)
		self.SetColumnWidth(1, 100)
		self.SetColumnWidth(2, 100)
		self.SetColumnWidth(3, 100)
		self.create_root()
		EVT_TREE_LIST_SET_CELL_VALUE(self, self.event_set_cell_value)
		EVT_TREE_LIST_SET_ITEM_IMAGE(self, self.event_set_item_image)
		EVT_TREE_LIST_SET_ITEM_DATA(self, self.event_set_item_data)

	def event_set_item_data(self, event):
		self.SetPyData(event.item, event.data)

	def event_set_item_image(self, event):
		for img, which in event.images:
			self.SetItemImage(event.item, img, which = which)

	def event_set_cell_value(self, event):
		self.SetItemText(event.item, event.value, event.col)

	def create_root(self):
		root_name = _('List Load/Send Catalogs & Files')
		root_desc = '........'
		self.root = self.AddRoot(root_name)
		self.SetPyData(self.root, [True, True, root_name, root_desc, '', 0, ''])
		#~ self.SetItemText(self.root, root_desc, 1)
		#~ self.SetItemImage(self.root, 0, which = wx.TreeItemIcon_Normal)
		#~ self.SetItemImage(self.root, 1, which = wx.TreeItemIcon_Expanded)
		self.items = [self.root]

	def clear(self):
		self.DeleteAllItems()
		self.create_root()

	def add_load_dir(self, path, item_name, full_path, dest = '', root = None):
		size = self.parent.connection.namespace.remote_getsize(full_path)
		data = {'complete':False, 'isdir':True, 'name':item_name, 'path':path, 'full_path':full_path, 'size':size, 'destination':dest}
		if root is None: root = self.root
		item = self.AppendItem(root, full_path)
		self.SetPyData(item, data)
		self.SetItemText(item, dest, 1)
		self.SetItemText(item, int_to_str(size), 3)
		self.SetItemImage(item, 4, which = wx.TreeItemIcon_Normal)
		self.SetItemImage(item, 5, which = wx.TreeItemIcon_Expanded)
		self.items.append(item)
		self.recursion_add_load_dir(full_path, create_full_path(dest, item_name), item)

	def recursion_add_load_dir(self, path, dest, root):
		for item in self.parent.connection.namespace.list_dir(path + '/'):
			full_path = create_full_path(path, item[1])
			size = item[2]
			data = {'complete':False, 'isdir':item[0], 'name':item[1], 'path':path, 'full_path':full_path, 'size':size, 'destination':dest}
			tree_item = self.AppendItem(root, item[1])
			self.SetPyData(tree_item, data)
			self.SetItemText(tree_item, dest, 1)
			self.SetItemText(tree_item, int_to_str(item[2]), 3)
			self.SetItemImage(tree_item, 5, which = wx.TreeItemIcon_Expanded)
			self.items.append(tree_item)
			if item[0]:
				self.SetItemImage(tree_item, 4, which = wx.TreeItemIcon_Normal)
				self.recursion_add_load_dir(item[3]+item[1]+'/', create_full_path(dest, item[1]), tree_item)
			else: self.SetItemImage(tree_item, 0, which = wx.TreeItemIcon_Normal)

	def add_send_dir(self, path, item_name, full_path, dest = '', root = None):
		size = os.path.getsize(full_path)
		data = {'complete':False, 'isdir':True, 'name':item_name, 'path':path, 'full_path':full_path, 'size':size, 'destination':dest}
		if root is None: root = self.root
		tree_item = self.AppendItem(root, full_path)
		self.SetPyData(tree_item, data)
		self.SetItemText(tree_item, dest, 1)
		self.SetItemText(tree_item, int_to_str(size), 3)
		self.SetItemImage(tree_item, 8, which = wx.TreeItemIcon_Normal)
		self.SetItemImage(tree_item, 9, which = wx.TreeItemIcon_Expanded)
		self.items.append(tree_item)
		self.recursion_add_send_dir(full_path, create_full_path(dest, item_name), tree_item)

	def recursion_add_send_dir(self, path, dest, root):
		list_dir = os.listdir(path)
		for item in list_dir:
			full_path = create_full_path(path, item)
			is_dir = os.path.isdir(full_path)
			size = os.path.getsize(full_path)
			data = {'complete':False, 'isdir':is_dir, 'name':item, 'path':path, 'full_path':full_path, 'size':size, 'destination':dest}
			tree_item = self.AppendItem(root, item)
			self.SetPyData(tree_item, data)
			self.SetItemText(tree_item, dest, 1)
			self.SetItemText(tree_item, int_to_str(size), 3)
			self.SetItemImage(tree_item, 9, which = wx.TreeItemIcon_Expanded)
			self.items.append(tree_item)
			if is_dir:
				self.SetItemImage(tree_item, 8, which = wx.TreeItemIcon_Normal)
				self.recursion_add_send_dir(full_path, create_full_path(dest, item), tree_item)
			else:
				self.SetItemImage(tree_item, 2, which = wx.TreeItemIcon_Normal)

# LOGGING CONTROL
class log_ctrl(wx.TextCtrl):
	def __init__(self, *args, **kwargs):
		self.file_name = kwargs.pop('file_name', 'log.txt')
		self.main_frame = kwargs.pop('main_frame', None)
		self.add_to_file = kwargs.pop('add_to_file', False)
		if self.main_frame is None:
			self.main_frame = args[0]
		super(log_ctrl, self).__init__(*args, **kwargs)
	def __write__(self, content):
		self.WriteText(content)
	def show_control(self, ctrl_name = 'log_ctrl'):
		if self.main_frame is not None:
			if hasattr(self.main_frame,'aui_manager'):
				self.main_frame.show_aui_pane_info(ctrl_name)
		self.SetInsertionPointEnd()
		if self.add_to_file: self.flush()
	def write(self, content):
		self.show_control()
		self.__write__(content)
	def writelines(self, l):
		self.show_control()
		map(self.__write__, l)
	def flush(self):
		self.SaveFile(self.file_name)

class rfb_main_frame(wx.Frame):
	def __init__(self, *args, **kwargs):
		self.app = kwargs.pop('app', None)
		self.connection = None
		self.flag_fill_tree = False

		wx.Frame.__init__(self, *args, **kwargs)
		self.SetIcon(wx.IconFromBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (32, 32))))

		#Logging Text Control
		self.log_ctrl = log_ctrl(self, style = wx.TE_MULTILINE)
		sys.stdout = self.log_ctrl
		sys.stderr = self.log_ctrl
		self.log = wx.LogTextCtrl(self.log_ctrl)
		self.log.SetLogLevel(wx.LOG_Error)
		wx.Log_SetActiveTarget(self.log)

		id_about = wx.ID_ABOUT
		id_exit = wx.ID_EXIT
		id_help = wx.ID_HELP
		id_find = wx.ID_FIND
		self.id_connect = wx.NewId()
		self.id_cancel_fill_tree = wx.NewId()
		id_disconnect = wx.NewId()
		id_load = wx.NewId()
		id_send = wx.NewId()
		id_load_dir = wx.NewId()
		id_send_dir = wx.NewId()
		self.id_remote_find = wx.NewId()
		self.id_cancel_remote_find = wx.NewId()
		id_clear_task_panel = wx.NewId()
		id_clear_task_tree_panel = wx.NewId()
		id_remote_delete = wx.NewId()
		id_remote_create_dir = wx.NewId()
		id_show_local_tree = wx.NewId()
		id_show_connect = wx.NewId()
		id_show_toolbar = wx.NewId()
		id_show_task_panel = wx.NewId()
		id_show_task_tree_panel = wx.NewId()
		id_show_search_panel = wx.NewId()
		id_show_log_ctrl = wx.NewId()

		img_size = (16, 16)
		bmp_quit = wx.ArtProvider_GetBitmap(wx.ART_QUIT, wx.ART_OTHER, img_size)
		bmp_about = wx.ArtProvider_GetBitmap(wx.ART_HELP_SETTINGS, wx.ART_OTHER, img_size)
		bmp_help = wx.ArtProvider_GetBitmap(wx.ART_HELP_BOOK, wx.ART_OTHER, img_size)
		bmp_toolbar = wx.ArtProvider_GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_OTHER, img_size)
		bmp_connect_param = wx.ArtProvider_GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, img_size)
		bmp_local_tree = wx.ArtProvider_GetBitmap(wx.ART_HELP_SIDE_PANEL, wx.ART_OTHER, img_size)
		bmp_task_panel = wx.ArtProvider_GetBitmap(wx.ART_PASTE, wx.ART_OTHER, img_size)
		bmp_show_search = wx.ArtProvider_GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_OTHER, img_size)
		self.bmp_remote_find = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_OTHER, img_size)
		self.bmp_cancel_remote_find = wx.ArtProvider_GetBitmap(wx.ART_ERROR, wx.ART_OTHER, img_size)
		self.bmp_net_dir = create_bmp_from_xpm(net_dir_xpm, img_size)
		self.bmp_cancel_net_dir = create_bmp_from_xpm(net_dir_xpm, img_size, ((2, '. c #FF0000'), ))
		bmp_closed_net_dir = create_bmp_from_xpm(closed_net_dir_xpm, img_size)
		bmp_load = create_bmp_from_xpm(load_xpm, img_size)
		bmp_loaded = create_bmp_from_xpm(load_xpm, img_size, ((2, '. c #FF0000'), ))
		bmp_send = create_bmp_from_xpm(send_xpm, img_size)
		bmp_sended = create_bmp_from_xpm(send_xpm, img_size, ((2, '. c #FF0000'), ))
		bmp_remote_delete = create_bmp_from_xpm(remote_delete_xpm, img_size)
		bmp_remote_create_dir = create_bmp_from_xpm(remote_create_dir_xpm)
		bmp_clear_task_panel = create_bmp_from_xpm(eraser_xpm)
		bmp_clear_task_tree_panel = create_bmp_from_xpm(eraser_xpm, repl = ((2, 'O c #9A9EF2'), ))
		bmp_load_dir = create_bmp_from_xpm(load_dir_xpm)
		bmp_loaded_dir = create_bmp_from_xpm(load_dir_xpm, repl = ((2, 'X c #FF0000'), ))
		bmp_load_dir_open = create_bmp_from_xpm(load_dir_open_xpm)
		bmp_loaded_dir_open = create_bmp_from_xpm(load_dir_open_xpm, repl = ((2, 'X c #FF0000'), ))
		bmp_send_dir = create_bmp_from_xpm(send_dir_xpm)
		bmp_sended_dir = create_bmp_from_xpm(send_dir_xpm, repl = ((2, 'o c #FF0000'), ))
		bmp_send_dir_open = create_bmp_from_xpm(send_dir_open_xpm)
		bmp_sended_dir_open = create_bmp_from_xpm(send_dir_open_xpm, repl = ((2, 'o c #FF0000'), ))
		bmp_log = create_bmp_from_xpm(log_xpm)

		self.menubar = wx.MenuBar()
		self.SetMenuBar(self.menubar)

		tmp_menu = wx.Menu()
		menu_item = wx.MenuItem(tmp_menu, self.id_connect, _('&Connect'), _('Connect to remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(self.bmp_net_dir)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_disconnect, _('&Disconnect'), _('Disconnect from remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_closed_net_dir)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_exit, _('&Quit'), _('Exit from this application'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_quit)
		tmp_menu.AppendItem(menu_item)
		self.menubar.Append(tmp_menu, _('Service'))

		tmp_menu = wx.Menu()
		menu_item = wx.MenuItem(tmp_menu, id_load, _('&Load'), _('Load item from remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_load)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_load_dir, _('Load dir'), _('Load item from remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_load_dir)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_send, _('&Send'), _('Send item to remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_send)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_send_dir, _('Send dir'), _('Send item to remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_send_dir)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, self.id_remote_find, _('&Find r.'), _('Find item on remote host'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(self.bmp_remote_find)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_remote_create_dir, _('Create dir'), _('Create remote dir'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_remote_create_dir)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_remote_delete, _('&Delete r.'), _('Delete remote item'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_remote_delete)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_clear_task_panel, _('&Clear all tasks'), _('Clear task panel'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_clear_task_panel)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_clear_task_tree_panel, _('Clear all dir tasks'), _('Clear task panel with tree'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_clear_task_tree_panel)
		tmp_menu.AppendItem(menu_item)
		self.menubar.Append(tmp_menu, _('File operations'))

		tmp_menu = wx.Menu()
		menu_item = wx.MenuItem(tmp_menu, id_show_toolbar, _('Show &toolbar'), _('Show main toolbar'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_toolbar)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_show_connect, _('Show &connect'), _('Show connect parameters'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_connect_param)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_show_local_tree, _('Show &local tree'), _('Show local tree file system'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_local_tree)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_show_task_panel, _('Show t&ask panel'), _('Show task panel'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_task_panel)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_show_task_tree_panel, _('Show task panel with tree'), _('Show task panel with tree'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_task_panel)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_show_search_panel, _('Show &search panel'), _('Show search panel'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_show_search)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_show_log_ctrl, _('Show &log'), _('Show log control'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_log)
		tmp_menu.AppendItem(menu_item)
		self.menubar.Append(tmp_menu, _('View'))

		tmp_menu = wx.Menu()
		menu_item = wx.MenuItem(tmp_menu, id_about, _('&About'), _('About authors'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_about)
		tmp_menu.AppendItem(menu_item)
		menu_item = wx.MenuItem(tmp_menu, id_help, _('&Help'), _('Help for this application'), wx.ITEM_NORMAL)
		menu_item.SetBitmap(bmp_help)
		tmp_menu.AppendItem(menu_item)
		self.menubar.Append(tmp_menu, _('Help'))

		self.main_toolbar = AuiToolBar(self, style = AUI_TB_DEFAULT_STYLE|AUI_TB_OVERFLOW)
		self.main_toolbar.AddTool(self.id_connect, _('Connect'), self.bmp_net_dir, wx.NullBitmap, wx.ITEM_NORMAL, _('Connect to remote host'), _('Connect to remote host'), None)
		self.main_toolbar.AddTool(id_disconnect, _('Disconnect'), bmp_closed_net_dir, wx.NullBitmap, wx.ITEM_NORMAL, _('Disconnect to remote host'), _('Disconnect to remote host'), None)
		self.main_toolbar.AddTool(id_load, _('Load'), bmp_load, wx.NullBitmap, wx.ITEM_NORMAL, _('Load item from remote host'), _('Load item from remote host'), None)
		self.main_toolbar.AddTool(id_send, _('Send'), bmp_send, wx.NullBitmap, wx.ITEM_NORMAL, _('Send item to remote host'), _('Send item to remote host'), None)
		self.main_toolbar.AddTool(id_load_dir, _('Load dir'), bmp_load_dir, wx.NullBitmap, wx.ITEM_NORMAL, _('Load item from remote host'), _('Load item from remote host'), None)
		self.main_toolbar.AddTool(id_send_dir, _('Send dir'), bmp_send_dir, wx.NullBitmap, wx.ITEM_NORMAL, _('Send item to remote host'), _('Send item to remote host'), None)
		self.main_toolbar.AddTool(self.id_remote_find, _('Find r.'), self.bmp_remote_find, wx.NullBitmap, wx.ITEM_NORMAL, _('Find item on remote host'), _('Find item on remote host'), None)
		self.main_toolbar.AddTool(id_remote_create_dir, _('Create dir'), bmp_remote_create_dir, wx.NullBitmap, wx.ITEM_NORMAL, _('Create remote dir'), _('Create remote dir'), None)
		self.main_toolbar.AddTool(id_remote_delete, _('Delete r.'), bmp_remote_delete, wx.NullBitmap, wx.ITEM_NORMAL, _('Delete remote item'), _('Delete remote item'), None)
		self.main_toolbar.AddTool(id_about, _('Authors'), bmp_about, wx.NullBitmap, wx.ITEM_NORMAL, _('Version application, author'), _('Version application, author'), None)
		self.main_toolbar.AddTool(id_exit, _('Exit'), bmp_quit, wx.NullBitmap, wx.ITEM_NORMAL, _('Exit from application'), _('Exit from application'), None)
		self.main_toolbar.Realize()

		#CONNECT PARAMETERS
		self.conn_panel = connect_panel(self)

		#LOAD OR SEND PROCESS
		self.task_panel = task_grid(self, (bmp_load, bmp_loaded, bmp_send, bmp_sended))
		dt = file_drop_target(self)
		self.task_panel.SetDropTarget(dt)

		self.task_tree_panel = task_tree(self, images = (bmp_load, bmp_loaded, bmp_send, bmp_sended, bmp_load_dir, bmp_load_dir_open, bmp_loaded_dir, bmp_loaded_dir_open, bmp_send_dir, bmp_send_dir_open, bmp_sended_dir, bmp_sended_dir_open))
		dt = file_drop_target(self)
		self.task_tree_panel.SetDropTarget(dt)

		#REMOTE TREE
		self.remote_tree = remote_tree_ctrl(self)
		dt = file_drop_target(self)
		self.remote_tree.SetDropTarget(dt)

		#LOCAL TREE
		self.local_tree = wx.GenericDirCtrl(self, wx.ID_ANY, style = wx.DIRCTRL_SHOW_FILTERS, filter = _('All files (*.*)|*.*|Python files (*.py)|*.py'))
		dt = py_drop_target(self)
		self.local_tree.SetDropTarget(dt)

		#SEARCH PANEL
		self.search_panel = search_panel(self)

		self.pane_captions = {
							'main_toolbar':('main_toolbar', _('Main toolbar')),
							'remote_tree':('remote_tree', _('Remote tree')),
							'local_tree':('local_tree', _('Local tree')),
							'connect_panel':('connect_panel', _('Connect parameters')),
							'task_panel':('task_panel', _('Task panel')),
							'search_panel':('search_panel', _('Search panel')),
							'task_tree_panel':('task_tree_panel', _('Task panel with tree')),
							'log_ctrl':('log_ctrl', _('log'))
							}
		self.aui_manager = AuiManager()
		self.aui_manager.SetManagedWindow(self)
		self.aui_manager.AddPane(self.main_toolbar, AuiPaneInfo().Name('main_toolbar').ToolbarPane().Top())#.Row(0).LeftDockable(False).RightDockable(False)
		self.aui_manager.AddPane(self.remote_tree, AuiPaneInfo().Name('remote_tree').CenterPane())
		self.aui_manager.AddPane(self.local_tree, AuiPaneInfo().Name('local_tree').Left().Layer(0).Position(0).Row(0).MaximizeButton(True).BestSize((300, 300)))
		self.aui_manager.AddPane(self.conn_panel, AuiPaneInfo().Name('connect_panel').Top().Layer(0).Position(0).Row(0).MaximizeButton(True).BestSize((150, 50)))
		self.aui_manager.AddPane(self.task_panel, AuiPaneInfo().Name('task_panel').Bottom().Layer(0).Position(0).Row(0).MaximizeButton(True).BestSize((400, 50)))
		self.aui_manager.AddPane(self.search_panel, AuiPaneInfo().Name('search_panel').Right().Layer(0).Position(0).Row(0).MaximizeButton(True).BestSize((300, 300)).Hide())
		self.aui_manager.AddPane(self.task_tree_panel, AuiPaneInfo().Name('task_tree_panel').Bottom().Layer(0).Position(1).Row(0).MaximizeButton(True).BestSize((400, 50)))
		self.aui_manager.AddPane(self.log_ctrl, AuiPaneInfo().Name('log_ctrl').Bottom().Layer(1).BestSize((100, 100)).Hide())

		if self.app.settings.ReadBool('GUI/load_default_perspective_on_start', True):
			self.aui_manager.LoadPerspective(self.app.settings.Read('GUI/perspective', ''))
		if self.log_ctrl.GetValue() != '':
			self.aui_manager.GetPane('log_ctrl').Show()
		self.aui_manager.Update()

		self.method_set_translation_pane_captions()

		self.sb = self.CreateStatusBar()

		wx.EVT_CLOSE(self, self.event_close)
		wx.EVT_MENU(self, id_exit, self.event_exit)
		wx.EVT_MENU(self, id_about, self.event_about)
		wx.EVT_MENU(self, id_help, self.event_help)
		wx.EVT_MENU(self, self.id_connect, self.event_connect)
		wx.EVT_MENU(self, id_disconnect, self.event_disconnect)
		wx.EVT_MENU(self, self.id_cancel_fill_tree, self.event_cancel_fill_tree)
		wx.EVT_MENU(self, id_load, self.event_load)
		wx.EVT_MENU(self, id_send, self.event_send)
		wx.EVT_MENU(self, id_load_dir, self.event_load_dir)
		wx.EVT_MENU(self, id_send_dir, self.event_send_dir)
		wx.EVT_MENU(self, self.id_remote_find, self.event_remote_find)
		wx.EVT_MENU(self, self.id_cancel_remote_find, self.event_cancel_remote_find)
		wx.EVT_MENU(self, id_remote_create_dir, self.event_remote_create_dir)
		wx.EVT_MENU(self, id_remote_delete, self.event_remote_delete)
		wx.EVT_MENU(self, id_clear_task_panel, self.event_clear_task_panel)
		wx.EVT_MENU(self, id_clear_task_tree_panel, self.event_clear_task_tree_panel)
		wx.EVT_MENU(self, id_show_toolbar, self.event_show_toolbar)
		wx.EVT_MENU(self, id_show_connect, self.event_show_connect)
		wx.EVT_MENU(self, id_show_local_tree, self.event_show_local_tree)
		wx.EVT_MENU(self, id_show_task_panel, self.event_show_task_panel)
		wx.EVT_MENU(self, id_show_task_tree_panel, self.event_show_task_tree_panel)
		wx.EVT_MENU(self, id_show_search_panel, self.event_show_search_panel)
		wx.EVT_MENU(self, id_show_log_ctrl, self.event_show_log_ctrl)
		#self.local_tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightUpLocalTree)
		#self.local_tree.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenuLocalDir)
		self.local_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnLocalItem)
		EVT_UPDATE_STATUS_BAR(self, self.event_update_status_bar)
		EVT_TOOL_BAR(self, self.event_tool_bar)

	def method_set_default_pane_captions(self):
		for name, caption in self.pane_captions.iteritems():
			self.aui_manager.GetPane(name).Caption(caption[0])

	def method_set_translation_pane_captions(self):
		for name, caption in self.pane_captions.iteritems():
			self.aui_manager.GetPane(name).Caption(caption[1])

	def method_load_default_state(self):
		frame_font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
		frame_font.SetNativeFontInfoFromString(self.app.settings.Read('GUI/font', ''))
		self.SetFont(frame_font)
		self.SetSize(eval(self.app.settings.Read('GUI/size', '(100,100)')))
		self.SetPosition(eval(self.app.settings.Read('GUI/position', '(100,100)')))
		centre_on_screen = eval(self.app.settings.Read('GUI/centre_on_screen', repr((False, wx.BOTH))))
		if centre_on_screen[0]:
			self.CentreOnScreen(centre_on_screen[1])
		self.Maximize(self.app.settings.ReadBool('GUI/maximized', False))
		self.Iconize(self.app.settings.ReadBool('GUI/iconized', False))
		self.ShowFullScreen(self.app.settings.ReadBool('GUI/fullscreen', False), self.app.settings.ReadInt('GUI/fullscreen_style', default_fullscreen_style))

	def method_save_default_state(self):
		flag_flush = False
		position = self.GetPositionTuple()
		if position != eval(self.app.settings.Read('GUI/position', '()')):
			self.app.settings.Write('GUI/position', repr(position))
			flag_flush = True
		size = self.GetSizeTuple()
		if size != eval(self.app.settings.Read('GUI/size', '()')):
			self.app.settings.Write('GUI/size', repr(size))
			flag_flush = True
		font = self.GetFont().GetNativeFontInfo().ToString()
		if font != self.app.settings.Read('GUI/font', ''):
			self.app.settings.Write('GUI/font', font)
			flag_flush = True
		is_maximized = self.IsMaximized()
		if is_maximized != self.app.settings.ReadBool('GUI/maximized', False):
			self.app.settings.WriteBool('GUI/maximized', is_maximized)
			flag_flush = True
		is_iconized = self.IsIconized()
		if is_iconized != self.app.settings.ReadBool('GUI/iconized', False):
			self.app.settings.WriteBool('GUI/iconized', is_iconized)
			flag_flush = True
		is_fullscreen = self.IsFullScreen()
		if is_fullscreen != self.app.settings.ReadBool('GUI/fullscreen', False):
			self.app.settings.WriteBool('GUI/fullscreen', is_fullscreen)
			flag_flush = True
		if flag_flush:
			self.app.settings.Flush()

	def method_save_default_perspective(self):
		self.method_set_default_pane_captions()
		current_perspective = self.aui_manager.SavePerspective()
		self.method_set_translation_pane_captions()
		if self.app.settings.Read('GUI/perspective', '') != current_perspective:
			self.app.settings.Write('GUI/perspective', current_perspective)
			self.app.settings.Flush()

	def event_update_status_bar(self, event):
		self.sb.SetStatusText(event.status_text)

	def event_tool_bar(self, event):
		event.toolbar.DeleteTool(event.delete_tool_id)
		event.toolbar.AddTool(
			#~ event.insert_pos,
			event.insert_tool_id,
			event.insert_caption,
			event.insert_bitmap1,
			event.insert_bitmap2,
			event.insert_tool_state,
			event.insert_desc1,
			event.insert_desc2,
			None)
		#~ event.toolbar.InsertLabelTool(
			#~ event.insert_pos,
			#~ event.insert_tool_id,
			#~ event.insert_caption,
			#~ event.insert_bitmap1,
			#~ event.insert_bitmap2,
			#~ event.insert_tool_state,
			#~ event.insert_desc1,
			#~ event.insert_desc2)
		event.toolbar.Realize()

	def show_aui_pane_info(self, name):
		if not self.aui_manager.GetPane(name).IsShown():
			self.aui_manager.GetPane(name).Show()
		self.aui_manager.Update()

	def show_hide_aui_pane_info(self, name):
		if self.aui_manager.GetPane(name).IsShown():
			self.aui_manager.GetPane(name).Hide()
		else:
			self.aui_manager.GetPane(name).Show()
		self.aui_manager.Update()

	def event_show_toolbar(self, event): self.show_hide_aui_pane_info('main_toolbar')
	def event_show_connect(self, event): self.show_hide_aui_pane_info('connect_panel')
	def event_show_local_tree(self, event): self.show_hide_aui_pane_info('local_tree')
	def event_show_task_panel(self, event): self.show_hide_aui_pane_info('task_panel')
	def event_show_task_tree_panel(self, event): self.show_hide_aui_pane_info('task_tree_panel')
	def event_show_search_panel(self, event): self.show_hide_aui_pane_info('search_panel')
	def event_show_log_ctrl(self, event): self.show_hide_aui_pane_info('log_ctrl')
	def event_clear_task_panel(self, event): self.task_panel.DeleteRows(numRows = self.task_panel.GetNumberRows())
	def event_clear_task_tree_panel(self, event): self.task_tree_panel.clear()

	def DoUpdate(self):
		self.aui_manager.Update()

	def event_exit(self, event):
		if self.app.settings.Read('Connect/server_host', '127.0.0.1') != self.conn_panel.txt_host.GetValue():
			self.app.settings.Write('Connect/server_host', self.conn_panel.txt_host.GetValue())
		if self.app.settings.ReadInt('Connect/server_port', 18812) != int(self.conn_panel.txt_port.GetValue()):
			self.app.settings.WriteInt('Connect/server_port', int(self.conn_panel.txt_port.GetValue()))
		if self.app.settings.Read('Connect/server_root', '/') != self.conn_panel.txt_remote_root.GetValue():
			self.app.settings.Write('Connect/server_root', self.conn_panel.txt_remote_root.GetValue())
		if self.app.settings.ReadInt('Connect/packet_size', 5242880) != int(self.conn_panel.txt_packet_size.GetValue()):
			self.app.settings.WriteInt('Connect/packet_size', int(self.conn_panel.txt_packet_size.GetValue()))
		self.Close()

	def event_close(self, event):
		if self.connection is not None:
			self.connection.close()
			self.connection = None
		if self.app.settings.ReadBool('GUI/save_default_state_on_exit', True):
			self.method_save_default_state()
		if self.app.settings.ReadBool('GUI/save_default_perspective_on_exit', True):
			self.method_save_default_perspective()
		self.main_toolbar.Destroy()
		self.aui_manager.UnInit()
		self.Destroy()

	def event_about(self, event):
		info = wx.AboutDialogInfo()
		info.Name = _('rfb - Remote File Browser')
		info.Version = self.app.app_version
		info.Copyright = _('(C) 2007-2009 Max Kolosov')
		info.Description = _('A "rfb" program is a software program \n'
			'that help work with network file system.\n\n'
			'Next operations is accessible:\n'
			'load file from network path;\n'
			'send file to network path;\n'
			'delete file from network path;\n'
			'search file on network path.')
		info.WebSite = ('http://saxi.nm.ru', _('rfb home page'))
		info.Developers = [_('Max Kolosov')]
		info.License = _('BSD license')
		wx.AboutBox(info)

	def event_help(self, event):
		print 'INFO:', 'not implemented'

	def start_socket(self):
		if self.connection == None:
			try:
				self.connection = create_client_socket(self.conn_panel.txt_host.GetValue(), int(self.conn_panel.txt_port.GetValue()))
			except BaseException, e:
				self.connection = None
				print 'ERROR:', e
			if self.connection is not None:
				#~ self.main_toolbar.DeleteTool(self.id_connect)
				#~ self.main_toolbar.InsertLabelTool(0, self.id_cancel_fill_tree, _('Stop tree'), self.bmp_cancel_net_dir, wx.NullBitmap, wx.ITEM_NORMAL, _('Stop fill tree'), _('Stop fill tree'))
				#~ self.main_toolbar.Realize()
				self.sb.SetStatusText(_('Connect success.'))
				create_remote_functions(self.connection)
				self.read_dir_tree()
				self.sb.SetStatusText(_('Remote folder ')+self.conn_panel.txt_remote_root.GetValue()+_(' reading.'))
				self.flag_fill_tree = True
			else: self.sb.SetStatusText(_('Not connected.'))
		else:
			self.read_dir_tree()
			self.sb.SetStatusText(_('Remote folder ')+self.conn_panel.txt_remote_root.GetValue()+_(' reading.'))
			self.remote_tree.UnselectAll()
			self.remote_tree.SelectItem(self.remote_tree.root)

	def stop_socket(self):
		self.remote_tree.clear()
		if self.connection is not None:
			self.connection.close()
			self.connection = None

	def event_cancel_fill_tree(self, event):
		self.flag_fill_tree = False

	def event_connect(self, event):
		self.start_socket()

	def event_disconnect(self, event):
		self.stop_socket()
		self.sb.SetStatusText(_('Connection closed.'))

	def send_or_load(self, load = True):
		if self.connection is not None:
			current_row = self.task_panel.GetGridCursorRow()
			path1 = self.task_panel.GetCellValue(current_row, 1)
			path2 = self.task_panel.GetCellValue(current_row, 2)
			file_size = self.task_panel.GetCellValue(current_row, 4).replace(' ', '')
			packet_size = self.conn_panel.txt_packet_size.GetValue().replace(' ', '')
			load_send = self.task_panel.GetCellValue(current_row, 0)
			if load_send == '0' and load:
				loading = True
				#~ if os.path.exists(path2):
					#~ m1 = path2 + _(' exists, overwrite?')
					#~ m2 = _('Warning')
					#~ if wx.MessageBox(m1, m2, wx.YES_NO) != wx.YES:
						#~ loading = False
				if loading:
					t = Thread(target = load_file, args = (self, current_row, path1, path2, int(file_size), int(packet_size)))
					t.setDaemon(True)
					t.start()
			elif load_send == '2' and not load:
				sending = True
				#~ if self.connection.namespace.path_exists(path2):
					#~ m1 = path2 + _(' exists, overwrite?')
					#~ m2 = _('Warning')
					#~ if wx.MessageBox(m1, m2, wx.YES_NO) != wx.YES:
						#~ sending = False
				if sending:
					t = Thread(target = send_file, args = (self, current_row, path1, path2, int(file_size), int(packet_size)))
					t.setDaemon(True)
					t.start()

	def event_load(self, event):
		self.send_or_load()

	def event_send(self, event):
		self.send_or_load(False)

	def event_load_dir(self, event):
		if self.connection is not None:
			root = self.task_tree_panel.GetRootItem()
			current = self.task_tree_panel.GetSelection()
			#current = self.task_tree_panel.GetCurrentItem()#only into new wx version
			if root.IsOk() and current.IsOk():
				if root == current:
					wx.MessageBox(_('Select valid item!'), _('Warning'))
				else:
					parent = self.task_tree_panel.GetItemParent(current)
					while parent != root:
						current = parent
						parent = self.task_tree_panel.GetItemParent(current)
					task = self.task_tree_panel.GetPyData(current)
					if task is not None:
						if not task['complete'] and task['isdir'] and remote_path_exists(self.connection, task['full_path']):
							t = Thread(target = recursion_load_file, args = (self.task_tree_panel, current, int(self.conn_panel.txt_packet_size.GetValue())))
							t.setDaemon(True)
							t.start()

	def event_send_dir(self, event):
		if self.connection is not None:
			root = self.task_tree_panel.GetRootItem()
			current = self.task_tree_panel.GetSelection()
			#current = self.task_tree_panel.GetCurrentItem()#only into new wx version
			if root.IsOk() and current.IsOk():
				if root == current:
					wx.MessageBox(_('Select valid item!'), _('Warning'))
				else:
					parent = self.task_tree_panel.GetItemParent(current)
					while parent != root:
						current = parent
						parent = self.task_tree_panel.GetItemParent(current)
					task = self.task_tree_panel.GetPyData(current)
					if task is not None:
						if not task['complete'] and task['isdir'] and os.path.exists(task['full_path']):
							t = Thread(target = recursion_send_file, args = (self.task_tree_panel, current, int(self.conn_panel.txt_packet_size.GetValue())))
							t.setDaemon(True)
							t.start()

	def remote_find(self):
		if self.connection is not None:
			self.search_panel.throb.Start()
			self.search_panel.not_stop_search_process = False
			#~ self.main_toolbar.DeleteTool(self.id_remote_find)
			#~ self.main_toolbar.InsertLabelTool(4, self.id_cancel_remote_find, _('Stop'), self.bmp_cancel_remote_find, wx.NullBitmap, wx.ITEM_NORMAL, _('Stop searching'), _('Stop searching service'))
			#~ self.main_toolbar.Realize()
			self.search_panel.search_ctrl.ShowSearchButton(False)
			self.search_panel.search_ctrl.ShowCancelButton(True)
			if not self.aui_manager.GetPane('search_panel').IsShown():
				self.aui_manager.GetPane('search_panel').Show()
			self.aui_manager.Update()
			path = self.search_panel.root_path.GetValue()
			svalue = self.search_panel.search_ctrl.GetValue()
			t = Thread(target = search_file_system_item, args = (self, path, svalue))
			t.setDaemon(True)
			t.start()
		else:
			self.sb.SetStatusText(_('Is not connection to remote host'))

	def cancel_remote_find(self):
		self.search_panel.not_stop_search_process = True
		self.main_toolbar.DeleteTool(self.id_cancel_remote_find)
		self.main_toolbar.InsertLabelTool(4, self.id_remote_find, _('Find'), self.bmp_remote_find, wx.NullBitmap, wx.ITEM_NORMAL, _('Find item on remote host'), _('Find item on remote host'))
		self.main_toolbar.Realize()
		self.search_panel.search_ctrl.ShowCancelButton(False)
		self.search_panel.search_ctrl.ShowSearchButton(True)
		self.search_panel.throb.Stop()

	def event_remote_find(self, event):
		self.remote_find()

	def event_cancel_remote_find(self, event):
		self.cancel_remote_find()

	def event_remote_delete(self, event):
		remote_item = self.remote_tree.GetSelection()
		if self.connection is not None and remote_item.IsOk():
			remote_item_name = self.remote_tree.GetItemText(remote_item, 0)
			remote_item_root = self.remote_tree.GetItemText(remote_item, 2)
			path = remote_item_root + remote_item_name
			if remote_path_exists(self.connection, path):
				delete_path(self.connection, path)
			if not remote_path_exists(self.connection, path):
				self.remote_tree.Delete(remote_item)

	def event_remote_create_dir(self, event):
		item = self.remote_tree.GetSelection()
		if self.connection is not None and item.IsOk():
			is_ok = True
			path = self.remote_tree.GetItemText(item, 2) + self.remote_tree.GetItemText(item, 0)
			if not remote_isdir(self.connection, path):
				item = self.remote_tree.GetItemParent(item)
				if item.IsOk():
					path = self.remote_tree.GetItemText(item, 2) + self.remote_tree.GetItemText(item, 0)
				else:
					is_ok = False
			if is_ok:
				dlg = wx.TextEntryDialog(self, path, _('New'), _('new_catalog'))
				if dlg.ShowModal() == wx.ID_OK:
					new_name = dlg.GetValue()
					if not new_name.isspace():
						new_path = create_full_path(path, new_name)
						new_path = new_path.replace('\\', '/')
						if self.connection.namespace.create_full_path(new_path):
							root_path = path + '/'
							for n in new_name.split('/'):
								item = self.remote_tree.AppendItem(item, n)
								self.remote_tree.SetItemText(item, '0', 1)
								self.remote_tree.SetItemText(item, root_path, 2)
								self.remote_tree.SetItemImage(item, 0, which = wx.TreeItemIcon_Normal)
								self.remote_tree.SetItemImage(item, 1, which = wx.TreeItemIcon_Expanded)
								self.remote_tree.items.append(item)
								root_path = n + '/'
				dlg.Destroy()

	def read_dir_tree(self, rem_dir = None):
		if rem_dir == None or rem_dir == '':
			rem_dir = self.conn_panel.txt_remote_root.GetValue().strip()
		if rem_dir is not '':
			if not rem_dir.endswith('/'):
				rem_dir += '/'
			elif not rem_dir.endswith('\\'):
				rem_dir += '/'
			rem_list = query_list_dir(self.connection, rem_dir)
			if rem_list is not None:
				host_name, port_value = self.connection.channel.stream.sock.getpeername()
				port_value = str(port_value)
				if wx.USE_UNICODE:
					host_name = unicode(host_name)#.decode(gui_codec)
					port_value = unicode(port_value)#.decode(gui_codec)
				#self.remote_tree.add_remote_list(rem_list, rem_dir, host_name+':'+port_value)
				self.remote_tree.add_remote_tree(rem_dir, host_name+':'+port_value)

	def OnAddQueueSend(self, event):
		src = self.local_tree.GetPath()
		if src == '' or os.path.isdir(src):
			self.sb.SetStatusText(_('Not selected local file!!!'))
		else:
			remote_item = self.remote_tree.GetSelection()
			if remote_item.IsOk():
				remote_root = self.remote_tree.GetItemText(self.remote_tree.root, 1)
				remote_item_name = self.remote_tree.GetItemText(remote_item, 0)
				if not remote_isdir(self.connection, remote_root+remote_item_name):
					self.sb.SetStatusText(_('Remote item must be folder!!!'))
				else:
					dst = remote_root+remote_item_name + '/' + os.path.split(src)[1]
					self.sb.SetStatusText(src+_(' --> load to --> ')+dst)
					if wx.USE_UNICODE:
						src = src.encode(gui_codec)
						dst = dst.encode(gui_codec)
					self.queue_send.append((src, dst))

	def OnRightUpLocalTree(self, event):
		if self.connection is not None:
			item = event.GetItem()
			if item:
				remote_item = self.remote_tree.GetSelection()
				if remote_item.IsOk():
					menu = wx.Menu()
					add_queue = menu.Append(wx.ID_ANY, _('Add to queue'))
					remote_item_name = self.remote_tree.GetItemText(remote_item, 0)
					send_to = menu.Append(wx.ID_ANY, _('Send to') + ' ' + remote_item_name)
					menu.AppendSeparator()
					self.Bind(wx.EVT_MENU, self.OnAddQueueSend, add_queue)
					#self.Bind(wx.EVT_MENU, self.OnSendTo, send_to)
					self.PopupMenu(menu)
					menu.Destroy()
				else:
					self.sb.SetStatusText(_('Not selected remote folder.'))
		event.Skip()

	def OnLocalItem(self, event):
		if self.connection == None:
			self.sb.SetStatusText(_('Connection closed.'))
		else:
			local_file = self.local_tree.GetPath()
			if local_file == '' or os.path.isdir(local_file):
				self.sb.SetStatusText(_('Not selected local file!!!'))
			else:
				remote_item = self.remote_tree.GetSelection()
				if remote_item.IsOk():
					remote_item_name = self.remote_tree.GetItemText(remote_item, 0)
					remote_root = self.remote_tree.GetItemText(remote_item, 2)
					dst_dir = remote_root+remote_item_name
					if not remote_isdir(self.connection, dst_dir):
						self.sb.SetStatusText(_('Remote item must be folder!!!'))
					else:
						source = local_file
						#~ destination = dst_dir + '/' + os.path.split(local_file)[1]
						destination = dst_dir + os.path.split(local_file)[1]
						self.sb.SetStatusText(source + _(' --> load to --> ') + destination)
						#if isinstance(src, unicode): src = src.encode(gui_codec)
						#if isinstance(dst, unicode): dst = dst.encode(gui_codec)
						self.task_panel.AppendRows()
						last_row = self.task_panel.GetNumberRows() - 1
						self.task_panel.SetCellValue(last_row, 0, '2')
						self.task_panel.SetCellValue(last_row, 1, source)
						self.task_panel.SetCellValue(last_row, 2, destination)
						self.task_panel.SetCellValue(last_row, 4, int_to_str(os.path.getsize(source)))
		event.Skip()

class server_frame(ShellFrame):
	def __init__(self, app):
		ShellFrame.__init__(self, size = (640, 480))
		self.shell.redirectStdin()
		self.shell.redirectStdout()
		self.shell.redirectStderr()
		self.app = app
		self.Bind(wx.EVT_ICONIZE, self.OnIconize)

	def __del__(self):
		self.app.ExitMainLoop()

	def OnIconize(self, event):
		self.Hide()

class task_bar_icon(wx.TaskBarIcon):

	TBMENU_CLOSE = wx.NewId()

	def __init__(self, app):
		wx.TaskBarIcon.__init__(self)
		self.app = app
		icon = self.MakeIcon(create_bmp_from_xpm(rfb_xpm).ConvertToImage())
		self.SetIcon(icon, _('rfb server') + ' ' + self.app.app_version)
		self.frm = server_frame(app)
		self.frm.Show(False)
		t = Thread(target = start_rpyc_server)
		t.setDaemon(True)
		t.start()
		self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
		self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

	def OnTaskBarActivate(self, evt):
		self.frm.Show(True)
		self.frm.Iconize(False)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		mitem = wx.MenuItem(menu, self.TBMENU_CLOSE, _('Close server'), _('Close remote python call server'), wx.ITEM_NORMAL)
		mitem.SetBitmap(wx.ArtProvider_GetBitmap(wx.ART_QUIT, wx.ART_OTHER, (16, 16)))
		menu.AppendItem(mitem)
		return menu

	def MakeIcon(self, img):
		if 'wxMSW' in wx.PlatformInfo:
			img = img.Scale(16, 16)
		elif 'wxGTK' in wx.PlatformInfo:
			img = img.Scale(22, 22)
		icon = wx.IconFromBitmap(img.ConvertToBitmap())
		return icon

	def OnTaskBarClose(self, evt):
		self.app.ExitMainLoop()


class rfb_app(wx.PySimpleApp):

	app_version = '0.7'
	app_path = os.getcwd()
	app_name = os.path.basename(sys.argv[0].split('.')[0])
	help_file = app_name + '.htb'
	settings_name = app_path + '/' + app_name + '.cfg'
	settings = open_settings(settings_name)

	def on_init(self):
		global _
		self.tbicon = None
		start_server = False
		if len(sys.argv) > 1:
			param = sys.argv[1]
			msg = ''
			if isinstance(param, unicode):
				param = str(param)
			if isinstance(sys.argv[1], str):
				if sys.argv[1] == 'server':
					start_server = True
				else:
					msg = _('usage: python %s server\nyou usage: %s') % (sys.argv[0], sys.argv[1])
			else:
				msg = _('usage: python %s server\nyou usage: not_string_parameter') % sys.argv[0]
			if len(msg) > 0:
				wx.MessageBox(msg, _('Warning'))
		name_user = wx.GetUserId()
		name_instance = 'rfb_client_wx::'
		if start_server:
			name_instance = 'rfb_server::'
		self.instance_checker = wx.SingleInstanceChecker(name_instance + name_user)
		if self.instance_checker.IsAnotherRunning():
			wx.MessageBox(_('Software is already running.'), _('Warning'))
			return False
		#~ wx.InitAllImageHandlers()
		if start_server:
			try:
				self.tbicon = task_bar_icon(self)
			except:
				return False
		else:
			self.mf = rfb_main_frame(None, app = self, title = _('Remote File Browser') + ' ' + self.app_version)
			self.SetTopWindow(self.mf)
			self.mf.Show()
		return True

	def OnExit(self):
		try:
			del self.instance_checker
		except:
			print_error()
		if self.tbicon is not None:
			self.tbicon.Destroy()

def main():
	app = rfb_app(0)
	if app.on_init():
		app.MainLoop()
	else:
		app.OnExit()

if __name__ == '__main__':
	main()
