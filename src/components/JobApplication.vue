<template>
  <router-link to="/applicants">View Applicants</router-link>
  <div class="job-application">
    <h2>Job Application Form</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">First Name:</label>
        <input type="text" id="firstName" v-model="formData.firstName" required>
      </div>
      <div class="form-group">
        <label for="name">Last Name:</label>
        <input type="text" id="lastName" v-model="formData.lastName" required>
      </div>
      <div class="form-group">
        <label for="name">Phone:</label>
        <input type="text" id="phone" v-model="formData.phone" required>
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" id="address" v-model="formData.address" required>
      </div>
      <div class="form-group">
        <label for="expectedSalary">Expected Salary:</label>
        <input type="number" id="expectedSalary" v-model="formData.expectedSalary" required>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name:'JobApplication',
  data() {
    return {
      formData:{
      firstName: '',
      lastName: '',
      phone: '',
      address: '',
      expectedSalary: null
      }
    }
  },
  methods: {
    async submitForm() {
       try {
        const response = await fetch('http://localhost:8000/submit_application', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            first_name: this.formData.firstName,
            last_name: this.formData.lastName,
            phone: this.formData.phone,
            address: this.formData.address,
            expected_salary: this.formData.expectedSalary
          })
          
        });
        if (response.ok){
        alert('Job Application Sent Successfully!.');

        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
    
  }
}
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
