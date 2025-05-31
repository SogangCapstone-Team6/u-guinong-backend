def build_prompt(state):
    system_prompt = """
    You are an agricultural expert specializing in helping young people who have returned to farming in rural areas. Based on the information provided, please give the best possible advice. But it should be only based on fact and given information. If you don't know, just say you don't know
    """
    
    prompt = [{"role": "system", "content": system_prompt}]
    prompt = prompt + state["messages"]
    
    if state["disease"]:
        prompt = prompt + [{"role": "system", "content": f"It seems to classified with {state['disease']}"}]

    if state["decision"] == "RAG":
        rag_prompt = "Here is some information you can refer\n"
        for data in state["retrived_data"]:
            rag_prompt = rag_prompt + data + "\n"
        prompt = prompt + [{"role": "system", "content": rag_prompt}]

    return prompt