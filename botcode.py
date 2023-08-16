from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from bot_database import all_k,all_v,insert_data,print_data,add_song
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
bot = Bot(token='your token')

storage= MemoryStorage()
dp = Dispatcher(bot,storage=storage)

class Form(StatesGroup):
    name=State()
class Form2(StatesGroup):
    link = State()
class myForm(StatesGroup):
    name = State()
class form_song_name(StatesGroup):
    song_name =State()
    
    
TEXT , TEXT2 = range(2)
NEW_TEXT = range(1)
#-----this is where i created buttons--------

button1= InlineKeyboardButton(text="AVAILABILITY",callback_data="back1")
button2= InlineKeyboardButton(text="ADD SONG",callback_data="back2")
button3 = InlineKeyboardButton(text="ADD NAME OF THE SONG",callback_data="back_name")
button4 = InlineKeyboardButton(text='ADD LINK OF THE SONG',callback_data="back_link")
button_sendme =InlineKeyboardButton(text="send me ",callback_data='send')
button_search = InlineKeyboardButton(text="SEARCH SONG",callback_data="back_search")
inline_keyboard=InlineKeyboardMarkup().add(button1,button2,button_search)
inline_keyboard2= InlineKeyboardMarkup().add(button3,button4)
inline_keyboard_send =InlineKeyboardMarkup().add(button_sendme)
#---------------commands :--------------------------------
@dp.message_handler(commands=['start'])
async def check(message: types.Message):
   await message.reply("""سلام به بات خوش امدید: 
https://t.me/freakysongz
لطفا جهت سرچ نام اهنگ را به فرمت زیر وارد کنین:
        
        /NameOfTheSong
        
        """,reply_markup=inline_keyboard)

@dp.message_handler(commands=['availability'])
async def bluh(message : types.Message):
    await message.reply(print_data())
    
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command"""

    current_state = await state.get_state()
    
    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Cancelled.')

@dp.message_handler(commands=['search_song'])
async def bluh(message : types.Message):
    await form_song_name.song_name.set()
    await message.reply("please send the name of the song : ")


def song_sender(name):
    @dp.message_handler(commands=[name])
    async def send_music2(message: types.Message):
        address = add_song(name) 
        await message.reply_audio(address,"@freakysongz")
        return address

#-------make buttons work : 

@dp.callback_query_handler(text=["back1"])
async def check_button(call: types.CallbackQuery):
    if call.data == "back1":
        await call.message.answer("here is our availble songs: ",)
        await call.message.answer(text=print_data())
        #await call.message.answer()
        
        
@dp.callback_query_handler(text =["back_search"])
async def search_song(call : types.CallbackQuery):
    if call.data == "back_search":
        await form_song_name.song_name.set()
        await call.message.reply("please send the name of the song : ")
        
@dp.callback_query_handler(text=["back2"])
async def check_button(call: types.CallbackQuery):
    if call.data == "back2":
        await call.message.answer(text='''FILL THESE TWO BUTTONS PLEASE : 
                                  
                                  @freakysongz''',reply_markup=inline_keyboard2)
@dp.callback_query_handler(text=["back_name","back_link"])
async def check_button(call: types.CallbackQuery):
        if call.data == "back_name":
            await Form.name.set()
            await call.message.reply("Send me name of the song : ") 
            #await call.message.answer()
        elif call.data == "back_link":
            await Form2.link.set()
            await call.message.reply("Send me link of the song : ") 
            await call.message.answer()  
@dp.callback_query_handler(text=["send"])
async def check_button(call: types.CallbackQuery):
    if call.data == "send":
        await myForm.name.set()
        await call.message.reply("send me the name of the song : ")


#----------------------recieve data from user :
@dp.message_handler(state=form_song_name.song_name)
async def process_name(message: types.Message,state: FSMContext):
    # Finish our conversation
    await state.finish()
    NEW_TEXT : str =message.text
    variable = add_song(NEW_TEXT)
    await message.reply_audio(variable,"@freakysongz") 
    if variable == False :
        await message.reply("not found")
    
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message,state: FSMContext):
    """Process user name"""
    """Process user link"""
    # Finish our conversation
    await state.finish()
    TEXT : str =message.text
    await message.reply(f"song's name is  {TEXT}") 
    
        
    @dp.message_handler(state=Form2.link)
    async def process_link(message: types.Message, state: FSMContext):
        """Process user link"""
        # Finish our conversation
        await state.finish()
        TEXT2 : str = message.text
        await message.reply(f"song's link is  {TEXT2}")
        insert_data(TEXT,TEXT2)
        
        
        
@dp.message_handler(state=myForm.name)
async def process_link(message: types.Message, state: FSMContext):
    """Process user link"""
    # Finish our conversation
    await state.finish()
    NEW_TEXT : str = message.text
    await message.reply(f"your song name is : {NEW_TEXT}")


executor.start_polling(dp)
