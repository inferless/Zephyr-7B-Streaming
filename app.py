import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"]='1'
from huggingface_hub import snapshot_download
import json
import numpy as np
import torch
from transformers import pipeline
from threading import Thread
from transformers import AutoTokenizer, TextIteratorStreamer
from awq import AutoAWQForCausalLM



class InferlessPythonModel:

    def initialize(self):
        model_id = "TheBloke/zephyr-7B-beta-AWQ"
        snapshot_download(repo_id=model_id,allow_patterns=["*.safetensors"])
        self.model = AutoAWQForCausalLM.from_quantized(model_id, fuse_layers=False, version="GEMV")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

    def infer(self, inputs, stream_output_handler):

        prompt = inputs["TEXT"]
        messages = [{ "role": "system", "content": "You are an agent that know about about cooking." }] 
        messages.append({ "role": "user", "content": prompt })
        tokenized_chat = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").cuda()
        generation_kwargs = dict(
            inputs=tokenized_chat,
            streamer=self.streamer,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            repetition_penalty=1.2,
            max_new_tokens=1024,
        )
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for new_text in self.streamer:
            output_dict = {}
            output_dict["OUT"] = new_text
            stream_output_handler.send_streamed_output(output_dict)
        thread.join()

        stream_output_handler.finalise_streamed_output()



    # perform any cleanup activity here
    def finalize(self,args):
        self.pipe = None
