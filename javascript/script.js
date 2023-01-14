function setPrompt(pre,post,tags, ...ckecked){
    prompts = []
    tags = JSON.parse(tags)

    if(pre != ""){
        prompts.push(pre)
    }
    ckecked.forEach((list,i) => {
        if(list.includes("Random")){
            if(list.length == 1){
                prompts.push("{"+tags[i].join("|")+"}")
            }
            else{
                prompts.push("{"+list.slice(1).join("|")+"}")
            }
        }
        else{
            prompts.push(...list)
        }
    })
    if(post != ""){
        prompts.push(post)
    }
    
    prompt = prompts.join(",")
    gradioApp().querySelector("#tab_txt2img #txt2img_prompt textarea").value = prompt
    gradioApp().querySelector('#tabs').querySelectorAll('button')[0].click()
    gradioApp().querySelector("#tab_txt2img #txt2img_prompt textarea").dispatchEvent(new Event("input", { bubbles: true }))
}