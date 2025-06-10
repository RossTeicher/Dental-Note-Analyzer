def generate_synthesia_script(procedure, language):
    base_script = {
        "English": f"Today, we're discussing your upcoming {procedure}. This procedure is important to preserve your oral health and ensure long-term comfort.",
        "Spanish": f"Hoy hablaremos sobre su procedimiento de {procedure}. Este procedimiento es importante para preservar su salud bucal.",
        "Russian": f"Сегодня мы обсудим процедуру {procedure}. Это важно для вашего здоровья полости рта.",
        "French": f"Aujourd'hui, nous parlons de votre procédure de {procedure}. Cette procédure est importante pour votre santé bucco-dentaire.",
        "Haitian Creole": f"Jodi a, nou pral pale sou pwosedi {procedure} ou a. Pwosedi sa a enpòtan pou sante dantè ou."
    }
    return base_script.get(language, base_script["English"])
