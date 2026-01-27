# 🚀 DEPLOY EN RAILWAY.APP - PASO A PASO

## 📦 ARCHIVOS EN ESTA CARPETA

```
railway-tracking/
├── tracking_server.py        # Servidor de tracking optimizado
├── requirements.txt           # Dependencias Python
├── Procfile                   # Configuración Railway
├── runtime.txt                # Versión Python
├── .gitignore                 # Archivos a ignorar
└── INSTRUCCIONES_DEPLOY_RAILWAY.md  # Este archivo
```

---

## 🎯 PASOS PARA DEPLOY (5 MINUTOS)

### PASO 1: Crear cuenta en Railway.app

1. Ve a: **https://railway.app**
2. Click en **"Start a New Project"** o **"Login"**
3. Usa tu cuenta de GitHub (recomendado) o email
4. Confirma tu email si te lo piden

---

### PASO 2: Crear nuevo proyecto

**Opción A: Deploy desde GitHub (Recomendado)**

1. Crea un repositorio en GitHub
2. Sube esta carpeta `railway-tracking/` al repositorio
3. En Railway: Click **"New Project"**
4. Click **"Deploy from GitHub repo"**
5. Selecciona tu repositorio
6. Railway detectará automáticamente Python y hará el deploy

**Opción B: Deploy directo (Más rápido para pruebas)**

1. En Railway: Click **"New Project"**
2. Click **"Deploy from GitHub repo"** → **"Deploy from local directory"**
3. O usa Railway CLI (más abajo)

---

### PASO 3: Deploy con Railway CLI (MÁS FÁCIL)

**Instalar Railway CLI:**

```bash
# En macOS (con Homebrew):
brew install railway

# O con npm:
npm install -g @railway/cli
```

**Hacer el deploy:**

```bash
# 1. Ve a la carpeta railway-tracking
cd railway-tracking

# 2. Login en Railway
railway login

# 3. Inicializar proyecto
railway init

# 4. Deploy!
railway up
```

**Obtener la URL pública:**

```bash
railway domain
```

Te dará una URL tipo:
```
https://tu-proyecto-production.up.railway.app
```

---

### PASO 4: Configurar dominio (opcional)

Si quieres usar tu propio dominio (h3l.ai o imagemia.ai):

1. En Railway, ve a tu proyecto
2. Click en **"Settings"** → **"Domains"**
3. Click **"Generate Domain"** (te da una URL .railway.app)
4. O click **"Custom Domain"** para usar h3l.ai

**Para custom domain:**
- Necesitas agregar un registro CNAME en Spaceship/DNS:
  ```
  Tipo: CNAME
  Nombre: tracking (quedará: tracking.h3l.ai)
  Valor: tu-proyecto.up.railway.app
  ```

---

## ✅ VERIFICAR QUE FUNCIONA

Una vez deployed, verifica:

1. **Abre la URL de Railway en navegador:**
   ```
   https://tu-proyecto.up.railway.app
   ```

   Deberías ver: "✅ Email Tracking Server - Servidor Activo"

2. **Verifica el endpoint de stats:**
   ```
   https://tu-proyecto.up.railway.app/stats
   ```

   Deberías ver el dashboard (vacío por ahora)

3. **Prueba el pixel de tracking:**
   ```
   https://tu-proyecto.up.railway.app/track/test123
   ```

   Debería cargar un pixel transparente

4. **Revisa stats de nuevo:**
   Deberías ver "test123" registrado con 1 apertura

---

## 🔧 DESPUÉS DEL DEPLOY

### Actualizar los templates de email

Una vez que tengas tu URL de Railway (ejemplo: `https://tu-proyecto.up.railway.app`), vuelve a la carpeta principal y ejecuta:

```bash
cd ..
python3 actualizar_templates_con_railway_url.py
```

O manualmente edita `templates_email_v6_CON_TRACKING.py` y cambia:

```python
# ANTES:
tracking_url = f"http://localhost:8888/track/{tracking_id}"

# DESPUÉS:
tracking_url = f"https://TU-PROYECTO.up.railway.app/track/{tracking_id}"
```

---

## 📊 VER ESTADÍSTICAS

**Desde cualquier lugar, 24/7:**

```
https://TU-PROYECTO.up.railway.app/stats
```

Verás:
- Total de aperturas
- Emails únicos abiertos
- Tabla con todos los detalles (ID, timestamp, IP, user-agent)

---

## 💰 COSTOS

**Railway Plan Gratuito:**
- ✅ $5 USD de crédito gratis al mes
- ✅ Suficiente para miles de trackings
- ✅ 500 horas de uptime/mes (más que suficiente)
- ✅ Base de datos SQLite incluida

**Si superas el plan gratuito:**
- Solo pagas lo que uses (~$0.000463/min)
- Para este uso (tracking), probablemente SIEMPRE sea gratis

---

## 🔍 MONITOREO

Railway te muestra en tiempo real:
- Logs de la aplicación
- Requests recibidos
- Errores (si los hay)
- Uso de recursos

**Ver logs:**
```bash
railway logs
```

O en el dashboard web de Railway.

---

## 🚨 TROUBLESHOOTING

### El deploy falla

**Error común:** "No Procfile found"
- **Solución:** Asegúrate que `Procfile` existe en la carpeta

**Error:** "Module not found"
- **Solución:** Verifica que `requirements.txt` tiene Flask y gunicorn

### La app no responde

**Revisa los logs:**
```bash
railway logs
```

**Verifica que el puerto esté correcto:**
Railway asigna automáticamente el puerto via variable `PORT`

### No se registran las aperturas

**Verifica que el pixel se carga:**
- Abre el email enviado
- Inspecciona el HTML (botón derecho → Ver código fuente)
- Busca: `<img src="https://...railway.app/track/..."`
- Copia esa URL y ábrela directamente en navegador
- Debería cargar un pixel transparente

---

## 📞 SIGUIENTE PASO

Una vez que tengas la URL de Railway funcionando:

1. **Anótala aquí:**
   ```
   Mi URL de Railway: https://______________________.up.railway.app
   ```

2. **Actualiza los templates** (te paso el script)

3. **Prueba enviando un email** a ti mismo

4. **Verifica que se registra** en /stats

5. **¡Listo para producción!** 🚀

---

## 🎉 BENEFICIOS DE RAILWAY

- ✅ Siempre disponible 24/7
- ✅ Escalable automáticamente
- ✅ HTTPS gratis
- ✅ Deploy en segundos
- ✅ Logs en tiempo real
- ✅ Base de datos persistente
- ✅ Probablemente gratis para siempre (bajo uso)

---

**¿Listo para hacer el deploy?** Sigue los pasos y avísame cuando tengas la URL de Railway.
