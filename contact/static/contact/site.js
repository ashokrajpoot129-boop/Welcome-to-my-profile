const form = document.querySelector('#contact-form');
const errorBox = document.querySelector('#form-error');

function getCookie(name) {
  const cookie = document.cookie.split('; ').find((part) => part.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : '';
}

form?.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.hidden = true;

  const button = form.querySelector('button[type="submit"]');
  const originalLabel = button.firstElementChild.textContent;
  button.disabled = true;
  button.firstElementChild.textContent = 'Sending...';

  try {
    const fields = new FormData(form);
    const response = await fetch(form.dataset.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        name: fields.get('name'),
        email: fields.get('email'),
        mobile_number: fields.get('mobile_number'),
        message: fields.get('message'),
      }),
    });
    const result = await response.json();
    if (!response.ok) {
      const firstError = Object.values(result.errors || {}).flat()[0];
      throw new Error(firstError?.message || result.error || 'Message could not be sent. Please try again.');
    }
    form.reset();
    errorBox.className = 'notice success';
    errorBox.textContent = result.message;
    errorBox.hidden = false;
  } catch (error) {
    errorBox.className = 'notice error';
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    button.disabled = false;
    button.firstElementChild.textContent = originalLabel;
  }
});