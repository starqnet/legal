"""
Gerador de CSV de Segurança dos Dados para Google Play Console
Uso: python3 generate_data_safety.py

Edite a seção TRUE_ROWS conforme os dados do app específico.
Template base: data_safety_template.csv (exportado do Play Console vazio)
"""
import csv, sys

APP_NAME = "quita"  # <- alterar para cada app

# Dados do app — editar conforme necessário
TRUE_ROWS = {
    # ── Etapa 2: configurações base (manter para todos os apps sem login) ──
    ("PSL_DATA_COLLECTION_COLLECTS_PERSONAL_DATA", ""),
    ("PSL_DATA_COLLECTION_ENCRYPTED_IN_TRANSIT", ""),
    ("PSL_SUPPORTED_ACCOUNT_CREATION_METHODS", "PSL_ACM_NONE"),
    ("PSL_SUPPORT_DATA_DELETION_BY_USER", "DATA_DELETION_NO"),

    # ── Etapa 3: tipos de dados coletados ──────────────────────────────────
    # Descomente conforme o app usar:
    ("PSL_DATA_TYPES_PERSONAL", "PSL_NAME"),                # Nome do usuário
    # ("PSL_DATA_TYPES_PERSONAL", "PSL_EMAIL"),             # E-mail
    ("PSL_DATA_TYPES_FINANCIAL", "PSL_PURCHASE_HISTORY"),   # Assinaturas (RevenueCat)
    ("PSL_DATA_TYPES_FINANCIAL", "PSL_OTHER"),              # Dados financeiros próprios do app
    ("PSL_DATA_TYPES_IDENTIFIERS", "PSL_DEVICE_ID"),        # ID dispositivo (RevenueCat)
    # ("PSL_DATA_TYPES_LOCATION", "PSL_APPROX_LOCATION"),   # Localização aproximada
    # ("PSL_DATA_TYPES_PHOTOS_AND_VIDEOS", "PSL_PHOTOS"),   # Fotos (somente se armazenadas fora do device)

    # ── Etapa 4: uso de Nome ────────────────────────────────────────────────
    ("PSL_DATA_USAGE_RESPONSES:PSL_NAME:PSL_DATA_USAGE_COLLECTION_AND_SHARING", "PSL_DATA_USAGE_ONLY_COLLECTED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_NAME:DATA_USAGE_USER_CONTROL", "PSL_DATA_USAGE_USER_CONTROL_REQUIRED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_NAME:DATA_USAGE_COLLECTION_PURPOSE", "PSL_APP_FUNCTIONALITY"),

    # ── Etapa 4: uso de dados financeiros do app ───────────────────────────
    ("PSL_DATA_USAGE_RESPONSES:PSL_OTHER:PSL_DATA_USAGE_COLLECTION_AND_SHARING", "PSL_DATA_USAGE_ONLY_COLLECTED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_OTHER:DATA_USAGE_USER_CONTROL", "PSL_DATA_USAGE_USER_CONTROL_REQUIRED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_OTHER:DATA_USAGE_COLLECTION_PURPOSE", "PSL_APP_FUNCTIONALITY"),

    # ── Etapa 4: histórico de compras (RevenueCat) ─────────────────────────
    ("PSL_DATA_USAGE_RESPONSES:PSL_PURCHASE_HISTORY:PSL_DATA_USAGE_COLLECTION_AND_SHARING", "PSL_DATA_USAGE_ONLY_COLLECTED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_PURCHASE_HISTORY:PSL_DATA_USAGE_COLLECTION_AND_SHARING", "PSL_DATA_USAGE_ONLY_SHARED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_PURCHASE_HISTORY:DATA_USAGE_USER_CONTROL", "PSL_DATA_USAGE_USER_CONTROL_OPTIONAL"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_PURCHASE_HISTORY:DATA_USAGE_COLLECTION_PURPOSE", "PSL_ACCOUNT_MANAGEMENT"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_PURCHASE_HISTORY:DATA_USAGE_SHARING_PURPOSE", "PSL_ACCOUNT_MANAGEMENT"),

    # ── Etapa 4: ID de dispositivo (RevenueCat) ────────────────────────────
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:PSL_DATA_USAGE_COLLECTION_AND_SHARING", "PSL_DATA_USAGE_ONLY_COLLECTED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:PSL_DATA_USAGE_COLLECTION_AND_SHARING", "PSL_DATA_USAGE_ONLY_SHARED"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_USER_CONTROL", "PSL_DATA_USAGE_USER_CONTROL_OPTIONAL"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_COLLECTION_PURPOSE", "PSL_ANALYTICS"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_COLLECTION_PURPOSE", "PSL_FRAUD_PREVENTION_SECURITY"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_COLLECTION_PURPOSE", "PSL_ACCOUNT_MANAGEMENT"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_SHARING_PURPOSE", "PSL_ANALYTICS"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_SHARING_PURPOSE", "PSL_FRAUD_PREVENTION_SECURITY"),
    ("PSL_DATA_USAGE_RESPONSES:PSL_DEVICE_ID:DATA_USAGE_SHARING_PURPOSE", "PSL_ACCOUNT_MANAGEMENT"),
}

FALSE_ROWS = {
    ("PSL_HAS_OUTSIDE_APP_ACCOUNTS", ""),
}

rows_out = []
with open("data_safety_template.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            rows_out.append(row)
            continue
        q_id = row[0] if len(row) > 0 else ""
        r_id = row[1] if len(row) > 1 else ""
        key = (q_id, r_id)
        if key in TRUE_ROWS:
            row[2] = "true"
        elif key in FALSE_ROWS:
            row[2] = "false"
        else:
            row[2] = ""
        rows_out.append(row)

out = f"{APP_NAME}_data_safety.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows_out)

marked = sum(1 for r in rows_out[1:] if len(r) > 2 and r[2] == "true")
print(f"✅ {out} gerado — {marked} campos marcados")
