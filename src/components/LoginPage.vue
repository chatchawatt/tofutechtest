<template>
<router-link to="/">Job Application</router-link>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" required>
      <br>
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required>
      <br>
      <button type="submit">Login</button>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error:''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });
        const data = await response.json();

        
        if (response.ok) {
          localStorage.setItem("authToken", data.token);
          this.$router.push('/applicants');
        } else if (response.status === 401) {
          this.error = "Invalid username or password";
        }else {
          this.error = data.message;
        }
      } catch (error) {
        console.error('Error logging in:', error);
        this.error = 'An error occurred while logging in. Please try again later.';
      }
    }
  }
};
</script>

<style scoped>
.job-application-form {
  max-width: 400px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
}
input[type="text"],
input[type="password"],
input[type="number"] {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
