
// ═══════════════════════════════════════════════════
// KORTEX — CONTACT FORM HANDLER v3.0
// Cleaned validation, safer errors, no fake success on failure
// ═══════════════════════════════════════════════════
const KORTEX_API_ENDPOINT = '/api/submit';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', handleFormSubmit);

  form.querySelectorAll('input, textarea, select').forEach((field) => {
    field.addEventListener('blur', () => validateField(field));
    field.addEventListener('focus', () => clearError(field));
    field.addEventListener('input', () => {
      const hasError = field.parentElement.querySelector('.form-error')?.textContent;
      if (hasError) validateField(field);
    });
  });

  const videoInput = form.querySelector('#video_url');
  if (videoInput) videoInput.addEventListener('input', debounce(previewYouTube, 450));
});

function validateField(field) {
  const errorEl = field.parentElement.querySelector('.form-error');
  let error = '';
  const value = field.value.trim();

  if (field.required && !value) {
    error = 'Ce champ est requis';
  } else if (field.type === 'email' && value && !isValidEmail(value)) {
    error = 'Adresse email invalide';
  } else if (field.type === 'url' && value && !isValidUrl(value)) {
    error = 'URL invalide';
  } else if (field.id === 'video_url' && value && !isYouTubeUrl(value)) {
    error = 'Ajoutez un lien YouTube valide';
  }

  field.classList.toggle('field-invalid', Boolean(error));
  field.classList.toggle('field-valid', !error && Boolean(value));
  if (errorEl) errorEl.textContent = error;
  return !error;
}

function clearError(field) {
  const errorEl = field.parentElement.querySelector('.form-error');
  if (errorEl) errorEl.textContent = '';
  field.classList.remove('field-invalid');
}

function previewYouTube(e) {
  const url = e.target.value.trim();
  removeYouTubePreview();
  if (!isYouTubeUrl(url)) return;
  const videoId = extractYouTubeId(url);
  if (!videoId) return;

  const preview = document.createElement('div');
  preview.id = 'yt-preview';
  preview.className = 'yt-preview';
  preview.innerHTML = `
    <img src="https://img.youtube.com/vi/${videoId}/mqdefault.jpg"
      alt="Thumbnail YouTube" width="80" height="56"
      style="object-fit: cover; border-radius: 2px; flex-shrink: 0;">
    <div>
      <p style="font-family: var(--ff-mono); font-size: 10px; color: var(--secondary); letter-spacing: 0.1em; margin-bottom: 4px;">SOURCE DÉTECTÉE</p>
      <p style="font-size: 13px; color: var(--text-primary);">Cette vidéo peut être transformée en <strong style="color: var(--primary);">articles + posts + FAQ</strong></p>
    </div>
  `;
  e.target.parentElement.appendChild(preview);
}

async function handleFormSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const fields = form.querySelectorAll('input[required], textarea[required], select[required]');
  let isValid = true;
  fields.forEach((field) => { if (!validateField(field)) isValid = false; });
  if (!isValid) {
    const firstError = form.querySelector('.form-error:not(:empty)');
    firstError?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  const submitBtn = form.querySelector('button[type="submit"]');
  const submitText = submitBtn.querySelector('.submit-text');
  const submitLoader = submitBtn.querySelector('.submit-loader');
  const messageEl = form.querySelector('.form-message');

  setLoadingState(submitBtn, submitText, submitLoader, true);
  showMessage(messageEl, 'neutral', 'Transmission du brief…');

  const payload = {
    client_name: `${form.querySelector('#firstname')?.value || ''} ${form.querySelector('#lastname')?.value || ''}`.trim(),
    client_email: form.querySelector('#email')?.value || '',
    company: form.querySelector('#company')?.value || '',
    plan: form.querySelector('#plan')?.value || '',
    video_url: form.querySelector('#video_url')?.value || '',
    message: form.querySelector('#message')?.value || '',
    client_tier: mapPlanToTier(form.querySelector('#plan')?.value || ''),
    source: 'website_contact_form',
    timestamp: new Date().toISOString()
  };

  try {
    const response = await fetch(KORTEX_API_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error(`API error: ${response.status}`);

    showMessage(messageEl, 'success', 'Brief reçu. Votre audit entre en file de traitement.');
    form.reset();
    removeYouTubePreview();
    form.querySelectorAll('.field-valid, .field-invalid').forEach((el) => {
      el.classList.remove('field-valid', 'field-invalid');
    });
  } catch (err) {
    console.warn('Submit failed:', err.message);
    showMessage(messageEl, 'error', 'Envoi impossible pour le moment. Branchez /api/submit ou réessayez plus tard.');
  } finally {
    setLoadingState(submitBtn, submitText, submitLoader, false);
  }
}

function setLoadingState(btn, textEl, loaderEl, loading) {
  btn.disabled = loading;
  textEl.style.display = loading ? 'none' : 'inline-block';
  loaderEl.style.display = loading ? 'inline-block' : 'none';
}

function showMessage(el, type, text) {
  el.textContent = text;
  el.style.display = 'block';
  if (type === 'success') {
    el.style.color = '#51cf66';
    el.style.borderColor = '#51cf66';
    el.style.background = 'rgba(81,207,102,0.08)';
  } else if (type === 'error') {
    el.style.color = '#ff6b6b';
    el.style.borderColor = '#ff6b6b';
    el.style.background = 'rgba(255,107,107,0.08)';
  } else {
    el.style.color = 'var(--text-primary)';
    el.style.borderColor = 'var(--secondary)';
    el.style.background = 'rgba(139,92,246,0.08)';
  }
}

function removeYouTubePreview() {
  document.getElementById('yt-preview')?.remove();
}

function mapPlanToTier(plan) {
  const map = { ghost: 'GHOST', swarm: 'SWARM', titan: 'TITAN', audit: 'AUDIT' };
  return map[plan] || 'AUDIT';
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidUrl(url) {
  try { new URL(url); return true; } catch { return false; }
}

function isYouTubeUrl(url) {
  return /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)[\w-]{11}/.test(url);
}

function extractYouTubeId(url) {
  const match = url.match(/(?:v=|youtu\.be\/|shorts\/)([\w-]{11})/);
  return match ? match[1] : null;
}

function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
