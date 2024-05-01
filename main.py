import os
import time
from fpy import print_results

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

while True:
  session = PromptSession()
  bindings = KeyBindings()

  @bindings.add('enter', eager=True)
  def _handle_enter(event):
    """ Handle enter key: insert new line or submit on double enter """
    buffer = event.current_buffer
    document = buffer.document

    if document.current_line == "":
      if document.line_count >= 2 and document.lines[-1] == "":
        buffer.validate_and_handle()
      else:
        buffer.insert_text('\n')
    else:
      buffer.newline(copy_margin=True)

  text = session.prompt(
    '>>>:\n', 
    multiline=True, 
    key_bindings=bindings
  )

  os.system("cls")
  time.sleep(0.5)
  
  try:
    print_results(text)
  except Exception as e:
    print(e)