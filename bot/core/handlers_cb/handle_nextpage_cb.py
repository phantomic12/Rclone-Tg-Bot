import logging as log
from bot.core.get_vars import get_val
from telethon.tl.types import KeyboardButtonCallback
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from bot.utils.list_selected_drive import get_list_drive_results, list_drive

async def next_page_menu(callback_query):
    _, offset = callback_query.data.decode().split(" ")
    log.info(f"NEXT_OFFSET: {offset}")
    data = get_val("JSON_RESULT_DATA")
    btn= []
    offset = int(offset)
    
    result, next_offset, total = await get_list_drive_results(data, offset=offset)

    btn.append([KeyboardButtonCallback(f" ✅ Seleccione esta Carpeta", f"mainmenu^selfdest")])

    list_drive(result, menu=btn, data_cb= "list_dir_main_menu")
        
    n_offset = int(next_offset)
    off_set = offset - 10 

    if offset == 0:
        btn.append(
            [KeyboardButtonCallback(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}", data="setting pages"),
             KeyboardButtonCallback("NEXT ⏩", data= f"next {next_offset}".encode("UTF-8"))
            ])

    elif offset >= total:
        btn.append(
             [KeyboardButtonCallback("⏪ BACK", data=f"next {off_set}"),
              KeyboardButtonCallback(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}",
                                   data="setting pages")])
    else:
        btn.append([KeyboardButtonCallback("⏪ BACK", data=f"next {off_set}"),
             KeyboardButtonCallback(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}", data="setting pages"),
             KeyboardButtonCallback("NEXT ⏩", data=f"next {n_offset}")
            ])
    try:
        mmes= await callback_query.get_message()
        d_rclone_drive= get_val("DEF_RCLONE_DRIVE")
        base_dir= get_val("BASE_DIR")
        await mmes.edit(f"Ruta:`{d_rclone_drive}:{base_dir}`", buttons=btn)
    except MessageNotModifiedError as e:
        log.info(e)
        pass
