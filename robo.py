import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from credenciais import EMAIL_LOGIN, SENHA_LOGIN

# ==========================================================
# 1. INICIAR O NAVEGADOR E A ESPERA
# ==========================================================
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

# ==========================================================
# 2. LOGIN E NAVEGAÇÃO ATÉ O E-MAIL MARKETING
# ==========================================================

# 2.1 Acessar o site
driver.get("https://horus.hiplatform.com/")
print("Acessando a página inicial...")

# 2.2 Clicar no botão azul CONTINUAR
try:
    print("Aguardando o botão CONTINUAR aparecer...")
    xpath_continuar = "//input[@value='Continuar']"
    btn_continuar = wait.until(EC.presence_of_element_located((By.XPATH, xpasth_continuar)))
    driver.execute_script("arguments[0].click();", btn_continuar)
    print("Botão CONTINUAR clicado com sucesso!")
except Exception as e:
    print(f"Aviso: Erro ao tentar clicar no Continuar (ou já passou dela): {e}")

time.sleep(3)

# 2.3 FAZER LOGIN COM O GOOGLE
MEU_EMAIL = EMAIL_LOGIN
MINHA_SENHA = SENHA_LOGIN

try:
    print("Procurando o botão do Google...")
    xpath_google = "//span[contains(@class, 'google-text')]"
    btn_google = wait.until(EC.presence_of_element_located((By.XPATH, xpath_google)))
    driver.execute_script("arguments[0].click();", btn_google)
    print("Botão do Google clicado! Aguardando a página do Google...")
    time.sleep(4) 
    
    # Preencher E-mail
    print("Digitando o e-mail...")
    campo_email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email'] | //*[@id='identifierId']")))
    campo_email.send_keys(MEU_EMAIL)
    
    btn_avancar_email = driver.find_element(By.XPATH, "//*[@id='identifierNext']//button")
    driver.execute_script("arguments[0].click();", btn_avancar_email)
    time.sleep(4)
    
    # Preencher Senha
    print("Digitando a senha...")
    campo_senha = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password'] | //*[@name='Passwd']")))
    campo_senha.send_keys(MINHA_SENHA)
    
    btn_avancar_senha = driver.find_element(By.XPATH, "//*[@id='passwordNext']//button")
    driver.execute_script("arguments[0].click();", btn_avancar_senha)
    
    print("Login do Google concluído com sucesso!")
    time.sleep(8) 

except Exception as e:
    print(f"⚠️ Aviso: Ocorreu um erro na etapa do Google (ou o login já estava ativo): {e}")

# ==========================================================
# 2.4 CLICAR EM 'FLOW' (Estratégia de Clique Real + Fallbacks)
# ==========================================================
from selenium.webdriver.common.action_chains import ActionChains

try:
    print("Verificando se a tela do produto 'Flow' está presente...")
    
    # Target 1: O span do ícone exatamente como no HTML enviado
    # Target 2: O span com o texto Flow
    # Target 3: Qualquer elemento clicável ao redor
    xpath_flow = (
        "//span[contains(@style, 'flow-')] | "
        "//span[contains(text(), 'Flow')] | "
        "//a[.//span[contains(text(), 'Flow')]]"
    )
    
    btn_flow = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, xpath_flow)))
    
    # 1. Scroll até o elemento
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_flow)
    time.sleep(1)
    
    # 2. Tativa de Clique Real com Mouse (Simula mover e clicar)
    try:
        actions = ActionChains(driver)
        actions.move_to_element(btn_flow).click().perform()
        print("Clique via ActionChains executado no 'Flow'!")
    except Exception:
        # 3. Fallback: Clique forçado via JS
        driver.execute_script("arguments[0].click();", btn_flow)
        print("Clique via JavaScript executado no 'Flow'!")
        
    time.sleep(8)
except Exception as e:
    print(f"Aviso: Não conseguiu clicar no Flow: {e}")

# ==========================================================
# 2.5 CLICAR NO MÓDULO 'E-MAIL MARKETING'
# ==========================================================
try:
    print("Procurando o módulo 'E-Mail Marketing' na tela inicial...")
    
    # Busca o card pelo svg emkt, pelo link que leva a modulo=EMK ou pelo texto exato
    xpath_emkt = (
        "//a[.//use[contains(@*,'#emkt')]] | "
        "//a[contains(@href, 'modulo=EMK')] | "
        "//a[contains(., 'E-Mail Marketing') or contains(., 'E-mail Marketing')]"
    )
    
    btn_emkt = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_emkt)))
    
    # Scroll até o elemento e clique duplo de garantia
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_emkt)
    time.sleep(1)
    
    try:
        btn_emkt.click()
    except:
        driver.execute_script("arguments[0].click();", btn_emkt)
        
    print("Módulo 'E-Mail Marketing' clicado com sucesso! Aguardando o carregamento da tabela...")
    time.sleep(12) # Tempo reforçado para carregar a tabela final
    
except Exception as e:
    print(f"⚠️ Erro ao tentar clicar em E-Mail Marketing: {e}")

# ==========================================================
# 3. CARREGAR MEMÓRIA DE AÇÕES JÁ PROCESSADAS
# ==========================================================
arquivo_historico = "historico_acoes.txt"
titulos_processados = set()

if os.path.exists(arquivo_historico):
    with open(arquivo_historico, "r", encoding="utf-8") as f:
        for linha in f:
            titulos_processados.add(linha.strip())
print(f"🧠 Memória carregada: {len(titulos_processados)} ações já estão salvas no histórico!")

# ==========================================================
# 4. LOOP DAS PÁGINAS (RODA ATÉ ACABAR AS SETINHAS VERDES)
# ==========================================================
pagina_atual = 1

while True:
    print(f"\n=======================================================")
    print(f"📄 INICIANDO PROCESSAMENTO DA PÁGINA {pagina_atual}")
    print(f"=======================================================")
    time.sleep(4) 
    
    try:
        print("Mapeando os disparos desta página...")
        xpath_todas_engrenagens = "//button[contains(@class, 'dropdown-toggle') and .//i[contains(@class, 'fa-gear')]]"
        
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_todas_engrenagens)))
        engrenagens = driver.find_elements(By.XPATH, xpath_todas_engrenagens)
        quantidade = len(engrenagens)
        
        print(f"Foram encontrados {quantidade} disparos na página {pagina_atual}!")

        for i in range(1, quantidade + 1):
            print(f"\n--- [Pág {pagina_atual}] Verificando linha {i} de {quantidade} ---")
            
            # ==========================================================
            # ESCUDO DE PROTEÇÃO DA LINHA
            # ==========================================================
            try:
                # Localizar a engrenagem desta linha
                xpath_engrenagem_atual = f"({xpath_todas_engrenagens})[{i}]"
                engrenagem_atual = wait.until(EC.presence_of_element_located((By.XPATH, xpath_engrenagem_atual)))
                
                # Pegar a linha completa da tabela (tr) para ler todas as colunas de uma vez
                linha_completa = engrenagem_atual.find_element(By.XPATH, "./ancestor::tr")
                
                # Tenta ler o título exato na Coluna 2
                try:
                    celula_titulo = linha_completa.find_element(By.XPATH, ".//td[2]")
                    titulo_acao = celula_titulo.text.strip()
                except:
                    titulo_acao = f"Linha_{pagina_atual}_{i}"
                
               # Checagem 1: Já está salvo na nossa memória?
                if titulo_acao in titulos_processados:
                    print(f"⏭️ JÁ PROCESSADO: '{titulo_acao}'. Pulando...")
                    continue
                
                # Checagem 2: É um rascunho sem envios?
                if "Não agendada" in linha_completa.text:
                    print(f"⏸️ RASCUNHO IGNORADO: A ação '{titulo_acao}' está como 'Não agendada'. Pulando...")
                    continue
                
                # Checagem 3: A ação já foi arquivada?
                if "Arquivada" in linha_completa.text:
                    print(f"🗂️ AÇÃO ARQUIVADA IGNORADA: A ação '{titulo_acao}' está como 'Arquivada'. Pulando...")
                    continue
                    
                print(f"🎯 NOVA AÇÃO: '{titulo_acao}'. Iniciando extração...")

                # Clicar na engrenagem
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", engrenagem_atual)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", engrenagem_atual)
                print("Engrenagem clicada. Aguardando o menu abrir...")
                time.sleep(2)
                
                # Clicar em 'Estatísticas'
                botoes_estatisticas = driver.find_elements(By.XPATH, "//span[contains(text(), 'Estatísticas')]")
                sucesso = False
                for botao in botoes_estatisticas:
                    if botao.is_displayed():
                        botao.click()
                        sucesso = True
                        break
                
                if not sucesso:
                    xpath_forcar = f"({xpath_todas_engrenagens})[{i}]/../..//span[contains(text(), 'Estatísticas')] | ({xpath_todas_engrenagens})[{i}]/following-sibling::ul//span[contains(text(), 'Estatísticas')]"
                    btn_forcado = driver.find_element(By.XPATH, xpath_forcar)
                    driver.execute_script("arguments[0].click();", btn_forcado)

                print("Indo para Estatísticas...")
                time.sleep(8)
                
                # Clicar na aba 'Acessos'
                aba_acessos = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Acessos')]")))
                driver.execute_script("arguments[0].click();", aba_acessos)
                print("Aba Acessos aberta.")
                time.sleep(3)
                
                # Clicar no ícone de "Mensagens não entregues"
                xpath_nao_entregues = "//tr[contains(., 'não entregues')]//span[contains(@class, 'glyphicon-user')] | //tr[contains(., 'não entregues')]//a"
                btn_nao_entregues = wait.until(EC.presence_of_element_located((By.XPATH, xpath_nao_entregues)))
                driver.execute_script("arguments[0].click();", btn_nao_entregues)
                print("Abrindo relação de Não entregues...")
                time.sleep(6)
                
                # Clicar em Exportar (no fim da página)
                xpath_exportar = "//a[contains(@href, 'estat_export_data')] | //div[normalize-space(text())='Exportar' and not(contains(text(), 'Interações'))]"
                btn_exportar = wait.until(EC.presence_of_element_located((By.XPATH, xpath_exportar)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_exportar)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", btn_exportar)
                print("Botão Exportar correto clicado.")
                time.sleep(4)
                
                # Selecionar "Incluir os contatos na lista"
                radio_incluir = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='listadd']")))
                driver.execute_script("arguments[0].click();", radio_incluir)
                print("Opção 'Incluir na lista' marcada.")
                time.sleep(1)
                
                # Selecionar a lista "OPT OUT GERAL"
                dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select")))
                select = Select(dropdown)
                select.select_by_visible_text("OPT OUT GERAL")
                print("Lista OPT OUT GERAL selecionada.")
                time.sleep(1)
                
                # Clicar em Avançar e lidar com o Alerta do Chrome
                btn_avancar = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Avançar') and contains(@class, 'btn')] | //button[contains(text(), 'Avançar')]")))
                driver.execute_script("arguments[0].click();", btn_avancar)
                print("Processando a inclusão...")
                
                try:
                    alerta = WebDriverWait(driver, 15).until(EC.alert_is_present())
                    alerta.accept()
                    print("Botão OK clicado com sucesso!")
                except:
                    print("Aviso: A janela de OK demorou muito ou sumiu, continuando...")
                
                # Salvar na memória
                titulos_processados.add(titulo_acao)
                with open(arquivo_historico, "a", encoding="utf-8") as f:
                    f.write(titulo_acao + "\n")
                print(f"💾 SALVO NA MEMÓRIA: '{titulo_acao}' registrado como concluído!")
                time.sleep(4)
                
                # Voltar para a tabela inicial
                try:
                    btn_voltar = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'E-Mail Marketing') or contains(text(), 'E-mail Marketing')] | //a[contains(., 'Página Inicial') or contains(., 'Voltar')]")))
                    driver.execute_script("arguments[0].click();", btn_voltar)
                    time.sleep(8)
                except:
                    driver.execute_script("window.history.go(-2);")
                    time.sleep(8)
                    
            except Exception as erro_linha:
                print(f"⚠️ Erro inesperado na ação '{titulo_acao}'. Ignorando e forçando retorno...")
                try:
                    btn_voltar_emergencia = driver.find_element(By.XPATH, "//span[contains(text(), 'E-Mail Marketing') or contains(text(), 'E-mail Marketing')]")
                    driver.execute_script("arguments[0].click();", btn_voltar_emergencia)
                    time.sleep(8)
                except:
                    try:
                        driver.execute_script("window.history.go(-1);")
                        time.sleep(8)
                    except:
                        pass
        
        # ==========================================================
        # 14. PRÓXIMA PÁGINA (Setinha Verde)
        # ==========================================================
        print(f"\n✅ Todas as {quantidade} linhas da Página {pagina_atual} foram verificadas!")
        print("Procurando o botão verde para ir para a próxima página...")
        
        try:
            btn_proxima_pagina = driver.find_element(By.XPATH, "//a[contains(@href, 'MudaPagina')]//img[contains(@src, 'ico_proximo')] | //img[contains(@src, 'ico_proximo')]/..")
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_proxima_pagina)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_proxima_pagina)
            
            pagina_atual += 1
            print(f"🚀 Clicado na setinha verde! Indo para a página {pagina_atual}...")
            time.sleep(8)
        except Exception as fim_paginas:
            print("\n🏁 Nenhuma setinha verde encontrada! O robô chegou à última página de todas!")
            break
            
    except Exception as erro_pagina:
        print(f"\n⚠️ Ocorreu um erro ao processar a página {pagina_atual}: {erro_pagina}")
        break

print("\n🎉 PROCESSO FINALIZADO! O robô fez todo o trabalho duro por você!")