document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Lỗi trong quá trình đăng nhập');
      }
      return response.json();
    })
    .then(data => {
      console.log('Đăng nhập thành công:', data);

      window.location.href = '/';
    })
    .catch(error => {
      console.error('Lỗi:', error);
    });
  });
  