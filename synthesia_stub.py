def generate_synthesia_script(procedure, language):
    base_script = {
        "English": f"Today, we're discussing your upcoming {procedure}. This procedure is important to preserve your oral health and ensure long-term comfort. Let's go over what to expect and how it helps you.",
        "Spanish": f"Hoy hablaremos sobre su procedimiento de {procedure}. Este procedimiento es importante para preservar su salud bucal y garantizar comodidad a largo plazo.",
        "Russian": f"Сегодня мы обсудим процедуру {procedure}. Это важно для сохранения здоровья полости рта и вашего комфорта в будущем.",
        "French": f"Aujourd'hui, nous parlons de votre procédure de {procedure}. Cette procédure est importante pour votre santé bucco-dentaire.",
        "Haitian Creole": f"Jodi a, nou pral pale sou pwosedi {procedure} ou a. Pwosedi sa a enpòtan pou sante dantè ou ak konfò alontèm ou."
    }
    return base_script.get(language, base_script["English"])
