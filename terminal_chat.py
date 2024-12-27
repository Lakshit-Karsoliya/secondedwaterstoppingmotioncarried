from transformers import AutoTokenizer , AutoModelForCausalLM
import re 
import torch
import colorama
import time
from PlayGround.run import *

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_path = "Qwen/Qwen2.5-Coder-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path,torch_dtype="auto",device_map=device)


def find_python(string):
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, string, re.DOTALL)
    if match:
        extracted_text = match.group(1) 
        return extracted_text
    else:
        return None
    
def colored(text,bright=True):
    return colorama.Style.BRIGHT+colorama.Fore.GREEN+text+colorama.Fore.RESET+colorama.Style.RESET_ALL

messages = [
        {"role": "system", "content": "You are Qwen. You are a helpful assistant."},
    ]



while True:
    prompt = input(colored('User : '))
    if prompt == '/bye':break
    prompt = prompt+""" if you need to write program write in ```python ``` block."""
    messages.append({
         "role":"user","content":prompt
    })
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
    )
    tensor = tokenizer.encode(text)
    tensor = torch.tensor([tensor]).to(device)
    max_tokens=1024
    past = None
    num_tokens=0
    total_time=0
    full_response=''
    model_response=''
    print(colored("Assistant : "),end='',flush=True)
    for i in range(max_tokens):
            st = time.time()
            with torch.no_grad():
                outputs = model(input_ids=tensor, past_key_values=past)
                logits = outputs.logits
                past = outputs.past_key_values
            ed=time.time()
            num_tokens+=1
            total_time+=(ed-st)
            logits = logits.detach()
            next_token_id = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
            decoded_token = tokenizer.decode(next_token_id[0])
            if decoded_token=="<|endoftext|>":
                break
            model_response+=decoded_token
            full_response+=decoded_token
            tensor=next_token_id.to(device)
            print(decoded_token,end='',flush=True)
            python_string = find_python(model_response)
            if (python_string is not None):
                write_file(python_string)
                feedback = play()
                append_string = f"{feedback}"
                print(append_string,end='',flush=True)
                full_response+=append_string
                tensor = torch.cat((tensor,torch.tensor([tokenizer.encode(append_string)]).to(device)),dim=1)
                model_response=''
    print()
    print("-"*100)
    avg_token_time=total_time/num_tokens
    print(f"Avrage time Per token {avg_token_time:.2f}")
    messages.append({
        "role":"assistant","content":full_response
    })
