from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
import torch

def textGeneratorGPT2(entrada):
    modelo = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    if not entrada:
        return "Error: Entrada vacía"

    try:
        max_length = tokenizer.model_max_length
        inputs = tokenizer.encode(entrada[:max_length], return_tensors='pt')
        
        if inputs.numel() == 0:
            return "Error: No se pudieron generar tokens"
        
        outputs = modelo.generate(
            inputs, 
            max_length=1000, 
            num_return_sequences=1,
            temperature=0.7, 
            top_k=40, 
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        
        texto_generado = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return texto_generado
    except Exception as e:
        return f"Error en la generación de texto: {str(e)}"
    
    
def textGeneratorFromMetaModel(entrada):
    model_id = "meta-llama/Llama-3.2-1B"
    
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    return pipe(entrada)
    
    

def textGeneratorFromMetaModelInstruct():
    model_id = "meta-llama/Llama-3.3-70B-Instruct"
    
    pipeline_model = pipeline(
        "text-generation",
        model=model_id,
        device_map="auto",
        model_kwargs={ "torch_dtype": torch.bfloat16 },
    )
    
    messages = [
        { "role": "system", "content": "You are a pirate chatbot who always responds in pirate speak" },
        { "role": "user", "content": "Who are you?" },
    ]
    
    ouputs = pipeline_model(
        messages,
        max_new_tokens=256
    )
    
    print(ouputs)
    return ouputs[0]["generated_text"][-1]