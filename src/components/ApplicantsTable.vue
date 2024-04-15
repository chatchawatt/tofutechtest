<template>
  <div class="applicants-table">
    <router-link to="/">Job Application</router-link>
    <button @click="logout" class="logout-btn">Logout</button>
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th v-for="header in headers" :key="header.value">{{ header.text }}</th>
             <th>
             <button @click="addApplicant()">New Record</button>
             <button @click="exportPdf()">Export</button>
             </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="index">
            <td v-for="header in headers" :key="header.value">{{ item[header.value] }}</td>
            <td>
            <button @click="editApplicant(item)">Edit</button>
            <button @click="deleteApplicant(item.id)">Delete</button>
          </td>
          </tr>
        </tbody>
      </table>
      <br>
      <label>Upload PDF</label>
      <br>
      <input type="file" @change="handleFileUpload">
      <div v-if="showEditPopup" class="edit-popup">
        <div class="popup-content">
          <h2>Edit Applicant</h2>
            <form @submit.prevent="submitEditApplicant">
              <div class="form-group">
                <label for="firstName">First Name:</label>
                <input type="text" id="firstName" v-model="selectedApplicantCopy.first_name" required>
              </div>
              <div class="form-group">
                <label for="lastName">Last Name:</label>
                <input type="text" id="lastName" v-model="selectedApplicantCopy.last_name" required>
              </div>
              <div class="form-group">
                <label for="phone">Phone:</label>
                <input type="text" id="phone" v-model="selectedApplicantCopy.phone" required>
              </div>
              <div class="form-group">
                <label for="address">Address:</label>
                <input type="text" id="address" v-model="selectedApplicantCopy.address" required>
              </div>
              <div class="form-group">
                <label for="expectedSalary">Expected Salary:</label>
                <input type="text" id="expectedSalary" v-model="selectedApplicantCopy.expected_salary" required>
              </div>
              
              <button type="submit">Save Changes</button>
              <button @click="cancelEdit()">Cancel</button>
            </form>
        </div>
      </div>
      <div v-if="newApplicant" class="edit-popup">
        <div class="popup-content">
          <h2>New Record</h2>
            <form @submit.prevent="submitNewApplicant">
              <div class="form-group">
                <label for="firstName">First Name:</label>
                <input type="text" id="firstName" v-model="formData.firstName" required>
              </div>
              <div class="form-group">
                <label for="lastName">Last Name:</label>
                <input type="text" id="lastName" v-model="formData.lastName" required>
              </div>
              <div class="form-group">
                <label for="phone">Phone:</label>
                <input type="text" id="phone" v-model="formData.phone" required>
              </div>
              <div class="form-group">
                <label for="address">Address:</label>
                <input type="text" id="address" v-model="formData.address" required>
              </div>
              <div class="form-group">
                <label for="expectedSalary">Expected Salary:</label>
                <input type="text" id="expectedSalary" v-model="formData.expectedSalary" required>
              </div>
              
              <button type="submit">Create</button>
              <button @click="cancelCreate()">Cancel</button>
            </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {

  data() {
    return {
      applicants: [], 
      items: [],
      headers: [ 
        { text: 'First Name', value: 'first_name' },
        { text: 'Last Name', value: 'last_name' },
        { text: 'Phone', value: 'phone' },
        { text: 'Address', value: 'address' },
        { text: 'Expected Salary', value: 'expected_salary' }
      ],
      formData:{
      firstName: '',
      lastName: '',
      phone: '',
      address: '',
      expectedSalary: null
      },
      showEditPopup: false,
      selectedApplicant: null,
      editingApplicant:null,
      selectedApplicantCopy:null,
      newApplicant:false
    }
  },
  created() {
    this.fetchApplicants();
  },
  methods: {
    async createApplicant(first_name, last_name, phone, address, expected_salary) {
      try {
        const response = await fetch('http://localhost:8000/submit_application', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            first_name,
            last_name,
            phone,
            address,
            expected_salary
          })
        });
        const data = await response.json();
        console.log(data); // Log response from backend
      } catch (error) {
        console.error('Error creating applicant:', error);
      }
    },
    async fetchApplicants() {
      try {
        const response = await fetch('http://localhost:8000/applicants');
        const data = await response.json();
        this.items = data;
      } catch (error) {
        console.error('Error fetching applicants:', error);
      }
    },
    async editApplicant(applicant){
      this.selectedApplicantCopy = {...applicant};
      this.editingApplicant = applicant;
      this.showEditPopup = true;

    },
    cancelEdit(){
      this.selectedApplicantCopy = null;
      this.editingApplicant = null;
      this.showEditPopup = false;
    },
    async addApplicant(){
      this.newApplicant = true;
    },
    cancelCreate(){
      this.newApplicant = false;
      this.formData.firstName = null;
      this.formData.lastName = null;
      this.formData.phone = null;
      this.formData.address = null;
      this.formData.expectedSalary = null;
    },

    async submitNewApplicant(){
      try {
        const response = await fetch(`http://localhost:8000/submit_application`, {
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
        alert('New Record Created!');
        this.cancelCreate();
        this.fetchApplicants();

        }
      } catch (error) {
        console.error('Error:', error);
      
      }

    },

    async submitEditApplicant() {
      try {
        const response = await fetch(`http://localhost:8000/applicants/${this.selectedApplicantCopy.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.selectedApplicantCopy)
        });
        if (response.ok) {
          alert('Changes saved successfully.');
          this.showEditPopup = false;
          this.fetchApplicants();
        } else {
          // Handle error response
        }
      } catch (error) {
        console.error('Error editing applicant:', error);
      }
      
      
    },

    async deleteApplicant(id) {
      if (confirm('Are you sure you want to delete this applicant?')) {
        try {
          await fetch(`http://localhost:8000/applicants/${id}`, {
            method: 'DELETE'
          });
          // Remove the deleted applicant from the list
          this.applicants = this.applicants.filter(applicant => applicant.id !== id);
          alert('Applicant deleted successfully.');
          window.location.reload();
        } catch (error) {
          console.error('Error deleting applicant:', error);
        }
      }
    },
    async exportPdf() {
    try {
        const response = await fetch('http://localhost:8000/export', {
            method: 'GET',
            headers: {
                Accept: 'application/pdf'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to download PDF');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'applicants.pdf');
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting PDF:', error);
    }
},
    async handleFileUpload(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8000/upload_pdf', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          alert('PDF uploaded successfully.');
          this.fetchApplicants()
        } else {
          throw new Error('Failed to upload PDF.');
        }
      } catch (error) {
        console.error('Error uploading PDF:', error);
      }
    },
    logout() {
      localStorage.removeItem("authToken");
      this.$router.push("/login");
    }
  }
}
</script>
<style scoped>
.applicants-table {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.logout-btn {
  margin-left: 20px;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.table-container {
  margin-top: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: left;
}

.table th {
  background-color: #f2f2f2;
  font-weight: bold;
}
.form-group {
  margin-bottom: 1rem;
}
</style>
