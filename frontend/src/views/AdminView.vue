<template>
  <div class="min-h-screen bg-slate-50 font-sans antialiased text-slate-800">
    <!-- Kurumsal Header ve Orijinal Bonna Logo Yerleşimi -->
    <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm select-none">
      <div class="flex items-center gap-4 cursor-pointer" @click="router.push('/dashboard')">
        <img src="https://bonna-website.b-cdn.net/bonnacloud-assets/BonnaCloud-Logo.png" alt="Bonna Cloud Logo" class="h-8 w-auto object-contain" />
        <h1 class="text-base font-black tracking-tight text-slate-900 border-l border-slate-200 pl-4">Control Center</h1>
      </div>
      
      <div class="flex gap-2 border border-slate-200 p-0.5 bg-slate-100 rounded-xl">
        <button @click="activeTab = 'users'" :class="activeTab === 'users' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-xs transition-all">Users Control</button>
        <button @click="activeTab = 'roles'" :class="activeTab === 'roles' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-xs transition-all">Roles & Permissions</button>
        <button @click="activeTab = 'cdn'" :class="activeTab === 'cdn' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-xs transition-all">CDN Engine</button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto p-6">
      <!-- 1. KULLANICI YÖNETİMİ SEKMESİ -->
      <section v-if="activeTab === 'users'" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-base font-black text-slate-900">User Master List</h2>
            <p class="text-xs text-slate-400 font-medium mt-0.5">Manage corporate credentials and assign access roles.</p>
          </div>
          <button @click="openUserModal(null)" class="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm active:scale-95">+ Add New User</button>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full text-left text-xs divide-y divide-slate-100">
            <thead>
              <tr class="text-slate-400 font-bold uppercase tracking-wider bg-slate-50/70">
                <th class="px-4 py-3 rounded-l-xl">Full Name</th>
                <th class="px-4 py-3">Email Address</th>
                <th class="px-4 py-3">Inherited Access Role</th>
                <th class="px-4 py-3">Status</th>
                <th class="px-4 py-3 rounded-r-xl w-24 text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50 font-medium text-slate-700">
              <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50/50">
                <td class="px-4 py-3.5 font-bold text-slate-900">{{ user.name }}</td>
                <td class="px-4 py-3.5 text-slate-500">{{ user.email }}</td>
                <td class="px-4 py-3.5">
                  <span class="px-2.5 py-1 bg-blue-50 border border-blue-100 text-blue-700 font-bold rounded-lg">{{ user.role_name }}</span>
                </td>
                <td class="px-4 py-3.5">
                  <span :class="user.isActive ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-red-50 text-red-700 border-red-100'" class="px-2 py-0.5 border rounded-md text-[10px] font-bold">{{ user.isActive ? 'ACTIVE' : 'BLOCKED' }}</span>
                </td>
                <td class="px-4 py-3.5 flex justify-center gap-1.5">
                  <button @click="openUserModal(user)" class="p-1.5 border border-slate-200 hover:border-slate-300 bg-white rounded-lg text-slate-600 hover:text-slate-900 shadow-sm">Edit</button>
                  <button @click="deleteUser(user.id)" class="p-1.5 border border-red-100 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg shadow-sm">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 2. ROL TABANLI YETKİLENDİRME SEKMESİ -->
      <section v-if="activeTab === 'roles'" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-base font-black text-slate-900">Roles & Directory Authorization Engine</h2>
            <p class="text-xs text-slate-400 font-medium mt-0.5">Define corporate roles and set Bunny CDN directory access rules globally.</p>
          </div>
          <button @click="openRoleModal(null)" class="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm active:scale-95">+ Add New Role</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="role in roles" :key="role.id" class="border border-slate-200 bg-slate-50/40 rounded-xl p-4 flex flex-col justify-between hover:shadow-md transition-all">
            <div>
              <div class="flex justify-between items-start">
                <h3 class="font-black text-slate-900 text-sm tracking-tight">{{ role.name }}</h3>
                <span class="text-[10px] bg-slate-200 text-slate-700 font-bold px-1.5 py-0.5 rounded">ID: {{ role.id }}</span>
              </div>
              <p class="text-[10px] text-slate-400 font-bold uppercase mt-3 tracking-wider">Authorized Folder Paths:</p>
              <div class="mt-1.5 space-y-1 max-h-32 overflow-y-auto pr-1">
                <div v-for="(f, i) in role.allowedFolders" :key="i" class="text-xs bg-white border border-slate-200 p-1.5 rounded-lg flex items-center justify-between shadow-sm">
                  <span class="font-bold text-slate-800 truncate max-w-[120px]" :class="f.allowed === false ? 'line-through text-red-500':''">{{ f.name }}</span>
                  <span class="text-[9px] font-bold px-1 rounded shadow-sm" :class="f.allowed === false ? 'bg-red-50 text-red-600':'bg-emerald-50 text-emerald-600'">{{ f.allowed === false ? 'Excluded':'Allowed' }}</span>
                </div>
                <p v-if="role.allowedFolders.length === 0" class="text-xs text-slate-400 italic">No directory permission assigned yet.</p>
              </div>
            </div>
            <div class="flex justify-end gap-1.5 mt-5 border-t border-slate-200/60 pt-3">
              <button @click="openRoleModal(role)" class="px-3 py-1.5 text-xs font-bold border border-slate-200 hover:border-slate-300 bg-white rounded-lg shadow-sm text-slate-700">Manage Rules</button>
              <button @click="deleteRole(role.id)" v-if="role.id !== 1" class="px-3 py-1.5 text-xs font-bold bg-red-50 text-red-600 hover:bg-red-100 border border-red-100 rounded-lg shadow-sm">Delete</button>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. CDN AYARLARI SEKMESİ -->
      <section v-if="activeTab === 'cdn'" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 max-w-xl mx-auto">
        <h2 class="text-base font-black text-slate-900 mb-1">Bunny.net CDN Node Configuration</h2>
        <p class="text-xs text-slate-400 font-medium mb-6">Link global cloud storage layers directly to the platform backend safely.</p>
        <form @submit.prevent="saveCdnSettings" class="space-y-4 text-xs font-bold">
          <div>
            <label class="block text-slate-600 mb-1.5">Storage Zone Name</label>
            <input v-model="cdnForm.storageName" type="text" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">Storage Access Key / Password</label>
            <input v-model="cdnForm.storagePassword" type="password" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">Pull Zone Base URL</label>
            <input v-model="cdnForm.pullZoneUrl" type="url" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">Storage Main Region Prefix (Optional)</label>
            <input v-model="cdnForm.region" type="text" placeholder="e.g. ny, sg, se (leave blank for Europe/Falkenstein)" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <button type="submit" class="w-full bg-slate-900 hover:bg-slate-800 text-white py-2.5 rounded-xl text-xs font-bold transition-all shadow-md active:scale-95">Commit CDN Updates</button>
        </form>
      </section>
    </main>

    <!-- ROL MODAL -->
    <div v-if="showRoleModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showRoleModal = false"></div>
      <div class="relative bg-white w-full max-w-4xl rounded-2xl shadow-2xl p-6 flex flex-col z-10 text-xs font-bold h-[88vh] animate-fade-in">
        <h3 class="text-sm font-black text-slate-900 mb-3">{{ roleForm.id ? 'Modify Role & Permissions' : 'Create Custom Access Role' }}</h3>
        
        <div class="space-y-3.5 flex-1 flex flex-col min-h-0 overflow-hidden">
          <div class="shrink-0">
            <label class="block text-slate-600 mb-1">Role Name</label>
            <input v-model="roleForm.name" type="text" placeholder="e.g. Tasarim_Ekibi, Musteri_A_Grubu" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          
          <div class="shrink-0 flex flex-col">
            <label class="block text-slate-600 mb-1.5">Hali Hazırda Yetki Verilmiş Dosya / Klasör Listesi</label>
            <div class="border border-slate-200 rounded-xl bg-slate-50 max-h-28 overflow-y-auto p-2 space-y-1.5 shadow-inner">
              <div v-for="(folder, idx) in roleForm.allowedFolders" :key="idx" class="flex items-center justify-between bg-white border border-slate-100 p-1.5 rounded-lg shadow-sm">
                <div class="flex items-center gap-2 overflow-hidden mr-2">
                  <span class="text-xs">{{ folder.mimeType === 'application/vnd.google-apps.folder' ? '📁' : '📄' }}</span>
                  <div class="truncate">
                    <span class="font-black text-slate-800 text-[11px] block truncate" :class="folder.allowed === false ? 'line-through text-red-400':''">{{ folder.name }}</span>
                    <span class="text-[9px] font-medium text-slate-400 block truncate tracking-tight">{{ folder.id || 'Root /' }}</span>
                  </div>
                </div>
                <button type="button" @click="roleForm.allowedFolders.splice(idx, 1)" class="text-red-600 hover:text-white border border-red-200 hover:bg-red-500 hover:border-red-500 px-2.5 py-1 rounded-md text-[10px] font-black transition-all shrink-0 shadow-sm active:scale-95">
                  Yetkiyi Kaldır
                </button>
              </div>
              <p v-if="roleForm.allowedFolders.length === 0" class="text-slate-400 font-medium italic text-center py-2.5 text-[10px]">Bu role tanımlanmış aktif bir yetki bulunmuyor.</p>
            </div>
          </div>

          <!-- BREADCRUMBS SİSTEMİ -->
          <div class="flex items-center gap-2 bg-slate-50 border border-slate-200 p-2 rounded-xl text-xs shrink-0 select-none">
            <button v-if="adminCurrentPath" type="button" @click="adminGoToParent" class="px-2 py-1 bg-white border border-slate-300 hover:bg-slate-100 rounded-lg text-[10px] font-bold shadow-sm">▲ Up</button>
            <span class="text-slate-400 font-bold">Location:</span>
            <span class="text-slate-900 font-black cursor-pointer hover:underline" @click="adminBrowseFolder('')">Home</span>
            <span v-for="(crumb, idx) in adminBreadcrumbs" :key="idx" class="flex items-center gap-1.5 text-slate-400">
              <span>/</span>
              <span class="text-slate-900 font-black cursor-pointer hover:underline truncate max-w-[120px]" @click="adminBrowseFolder(crumb.path)">{{ crumb.name }}</span>
            </span>
          </div>

          <!-- ANA EKRAN İKİZİ LİSTE TABLOSU -->
          <div class="flex-1 overflow-y-auto border border-slate-100 bg-white shadow-inner rounded-xl min-h-0">
            <div v-if="loadingFolders" class="flex flex-col items-center py-12 justify-center text-slate-400">
              <div class="w-5 h-5 border-2 border-slate-300 border-t-slate-800 rounded-full animate-spin mb-2"></div>
              <p class="text-[10px] font-medium">Opening cloud folder layer...</p>
            </div>

            <table class="min-w-full divide-y divide-slate-100 text-left text-sm" v-else>
              <thead>
                <tr class="text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-50/70 select-none">
                  <th scope="col" class="pl-4 py-2 w-8 rounded-l-xl">Select</th>
                  <th scope="col" class="pl-3 py-2">File Name</th>
                  <th scope="col" class="px-3 py-2 w-24">Size</th>
                  <th scope="col" class="px-3 py-2 w-24 rounded-r-xl">Type</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-for="item in adminItems" :key="item.id" @click="item.mimeType === 'application/vnd.google-apps.folder' ? adminBrowseFolder(item.id) : null" class="hover:bg-slate-50/50 cursor-pointer group transition-colors">
                  <td class="pl-4 py-2 w-8" @click.stop>
                    <input type="checkbox" :id="'item_' + item.id" :checked="isItemChecked(item.id)" @change="handleItemToggle($event, item)" class="w-3.5 h-3.5 rounded text-slate-900 border-slate-300 focus:ring-0 cursor-pointer shadow-sm" />
                  </td>
                  
                  <td class="pl-2 pr-4 py-1.5 font-semibold text-slate-700 whitespace-nowrap flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-md overflow-hidden flex items-center justify-center shrink-0 border border-slate-100 bg-white relative shadow-sm select-none">
                      <span v-if="item.mimeType === 'application/vnd.google-apps.folder'" class="text-sm">📁</span>
                      <span v-else-if="isImage(item.name)" class="text-sm">📷</span>
                      <span v-else-if="isVideo(item.name)" class="text-sm">🎬</span>
                      <span v-else-if="isPDF(item.name)" class="text-[9px] text-red-600 font-black tracking-tighter">PDF</span>
                      <span v-else class="text-sm">📄</span>
                    </div>
                    <div class="truncate flex flex-col">
                      <span class="truncate text-[11px] font-bold text-slate-800 max-w-[320px] group-hover:text-blue-600 transition-colors">{{ item.name }}</span>
                    </div>
                  </td>
                  
                  <td class="px-3 py-1.5 text-slate-500 text-[11px] font-bold">
                    {{ item.mimeType === 'application/vnd.google-apps.folder' ? '--' : formatSize(item.size) }}
                  </td>
                  <td class="px-3 py-1.5 text-slate-400 text-[10px] font-bold uppercase rounded-r-xl">
                    {{ item.mimeType === 'application/vnd.google-apps.folder' ? 'Folder' : getExtension(item.name) }}
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="adminItems.length === 0 && !loadingFolders" class="text-slate-400 italic text-center py-12 text-xs">This directory is empty.</div>
          </div>
        </div>
        
        <div class="flex justify-end gap-2 mt-3 border-t border-slate-100 pt-3 shrink-0">
          <button @click="showRoleModal = false" class="px-4 py-2 border border-slate-200 bg-white rounded-xl text-slate-700">Cancel</button>
          <button @click="saveRole" class="px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl">Commit Changes</button>
        </div>
      </div>
    </div>

    <!-- KULLANICI MODAL -->
    <div v-if="showUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showUserModal = false"></div>
      <div class="relative bg-white w-full max-w-md rounded-2xl shadow-2xl p-6 z-10 text-xs font-bold">
        <h3 class="text-sm font-black text-slate-900 mb-4">{{ userForm.id ? 'Modify System Credentials' : 'Register New Secure Member' }}</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-slate-600 mb-1.5">User Full Name</label>
            <input v-model="userForm.name" type="text" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">Email Address</label>
            <input v-model="userForm.email" type="email" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">Account Password {{ userForm.id ? '(Leave blank to keep same)' : '' }}</label>
            <input v-model="userForm.password" type="password" :required="!userForm.id" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-slate-600 mb-1.5">Core Group Type</label>
              <select v-model="userForm.role" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white">
                <option value="müşteri">Müşteri (Customer)</option>
                <option value="ekip">Şirket Ekibi (Team)</option>
                <option value="admin">Yönetici (Admin)</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-600 mb-1.5">Assign Access Role</label>
              <select v-model="userForm.role_id" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-bold text-blue-700 focus:outline-none focus:border-slate-900 focus:bg-white">
                <option :value="null">No Role (Access Denied)</option>
                <option v-for="r in roles" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>
          </div>
          <div class="flex items-center gap-2 pt-2">
            <input v-model="userForm.isActive" type="checkbox" id="userActiveChk" class="w-4 h-4 text-slate-900 rounded border-slate-300" />
            <label for="userActiveChk" class="text-slate-700 cursor-pointer select-none">Authorize active access permission to this user</label>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6 border-t border-slate-100 pt-4">
          <button @click="showUserModal = false" class="px-4 py-2 border border-slate-200 bg-white rounded-xl text-slate-700">Cancel</button>
          <button @click="saveUser" class="px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl">Commit Credentials</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const activeTab = ref("users")

const users = ref([])
const roles = ref([])
const adminItems = ref([]) 
const adminCurrentPath = ref("") 
const loadingFolders = ref(false)

const showUserModal = ref(false)
const showRoleModal = ref(false)

const cdnForm = ref({ storageName: "", storagePassword: "", pullZoneUrl: "", region: "" })
const userForm = ref({ id: null, name: "", email: "", password: "", role: "müşteri", role_id: null, isActive: true })
const roleForm = ref({ id: null, name: "", allowedFolders: [] })

const fetchAllData = async () => {
  try {
    const uResp = await axios.get(`${window.location.origin}/api/users`)
    users.value = uResp.data
    const rResp = await axios.get(`${window.location.origin}/api/roles`)
    roles.value = rResp.data
    const cResp = await axios.get(`${window.location.origin}/api/cdn`)
    cdnForm.value = cResp.data
  } catch (err) {
    alert("Authorization node sync error.")
  }
}

const adminBrowseFolder = async (targetPath = "") => {
  loadingFolders.value = true
  adminItems.value = []
  try {
    const response = await axios.get(`${window.location.origin}/files?path=${encodeURIComponent(targetPath)}`)
    adminItems.value = response.data.files || []
    adminCurrentPath.value = targetPath
  } catch (err) {
    console.error("Folder exploration failed:", err)
  } finally {
    loadingFolders.value = false
  }
}

const adminGoToParent = () => {
  if (!adminCurrentPath.value) return
  const parts = adminCurrentPath.value.split('/')
  parts.pop()
  adminBrowseFolder(parts.join('/'))
}

const adminBreadcrumbs = computed(() => {
  if (!adminCurrentPath.value) return []
  const parts = adminCurrentPath.value.split('/')
  const list = []
  let acc = ""
  for (const p of parts) {
    if (p) {
      acc = acc ? `${acc}/${p}` : p
      list.push({ name: p, path: acc })
    }
  }
  return list
})

const isItemChecked = (itemId) => {
  const found = roleForm.value.allowedFolders.find(f => f.id === itemId)
  if (found) return found.allowed === true
  const parts = itemId.split('/')
  for (let i = parts.length - 1; i > 0; i--) {
    const parentPath = parts.slice(0, i).join('/')
    const parentFound = roleForm.value.allowedFolders.find(f => f.id === parentPath)
    if (parentFound) {
      return parentFound.allowed === true
    }
  }
  return false
}

// 🌟 GÜNCELLEME: BOYUT (SIZE) PARAMETRESİNİ DE HAFIZAYA ALAN METOT
const handleItemToggle = (event, item) => {
  const newState = event.target.checked
  roleForm.value.allowedFolders = roleForm.value.allowedFolders.filter(f => f.id !== item.id)
  let inheritedState = false
  const parts = item.id.split('/')
  for (let i = parts.length - 1; i > 0; i--) {
    const parentPath = parts.slice(0, i).join('/')
    const parentFound = roleForm.value.allowedFolders.find(f => f.id === parentPath)
    if (parentFound) {
      inheritedState = parentFound.allowed === true
      break
    }
  }
  if (newState !== inheritedState) {
    roleForm.value.allowedFolders.push({
      id: item.id,
      name: item.name,
      mimeType: item.mimeType,
      size: item.size || 0, // Dosyanın gerçek boyutunu burada mühürle!
      allowed: newState
    })
  }
  if (item.mimeType === 'application/vnd.google-apps.folder') {
    adminItems.value.forEach(child => {
      if (child.id.startsWith(item.id + '/')) {
        roleForm.value.allowedFolders = roleForm.value.allowedFolders.filter(f => f.id !== child.id)
      }
    })
  }
}

const openRoleModal = async (role = null) => {
  if (role) {
    roleForm.value = { id: role.id, name: role.name, allowedFolders: JSON.parse(JSON.stringify(role.allowedFolders)) }
  } else {
    roleForm.value = { id: null, name: "", allowedFolders: [] }
  }
  showRoleModal.value = true
  await adminBrowseFolder("") 
}

const saveRole = async () => {
  if (!roleForm.value.name.trim()) return alert("Role name is required.")
  try {
    if (roleForm.value.id) {
      await axios.put(`${window.location.origin}/api/roles/${roleForm.value.id}`, roleForm.value)
    } else {
      await axios.post(`${window.location.origin}/api/roles`, roleForm.value)
    }
    showRoleModal.value = false
    fetchAllData()
  } catch (err) { alert(err.response?.data?.detail || "Role save failed.") }
}

const deleteRole = async (id) => {
  if (!confirm("Are you sure you want to completely purge this access role?")) return
  try {
    await axios.delete(`${window.location.origin}/api/roles/${id}`)
    fetchAllData()
  } catch (err) { alert("Purge aborted.") }
}

const isVideo = (filename) => ['mp4', 'webm', 'ogg', 'mov', 'avi'].includes(filename.split('.').pop().toLowerCase())
const isImage = (filename) => ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'tiff', 'tif'].includes(filename.split('.').pop().toLowerCase())
const isPDF = (filename) => filename.split('.').pop().toLowerCase() === 'pdf'
const getExtension = (filename) => filename.split('.').pop().toUpperCase()

const formatSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const openUserModal = (user = null) => {
  if (user) {
    userForm.value = { id: user.id, name: user.name, email: user.email, password: "", role: user.role, role_id: user.role_id, isActive: user.isActive }
  } else {
    userForm.value = { id: null, name: "", email: "", password: "", role: "müşteri", role_id: roles.value[0]?.id || null, isActive: true }
  }
  showUserModal.value = true
}

const saveUser = async () => {
  try {
    if (userForm.value.id) {
      await axios.put(`${window.location.origin}/api/users/${userForm.value.id}`, userForm.value)
    } else {
      await axios.post(`${window.location.origin}/api/users`, userForm.value)
    }
    showUserModal.value = false
    fetchAllData()
  } catch (err) { alert(err.response?.data?.detail || "Credential modification error.") }
}

const deleteUser = async (id) => {
  if (!confirm("Delete this user permanently from cloud registry?")) return
  try {
    await axios.delete(`${window.location.origin}/api/users/${id}`)
    fetchAllData()
  } catch (err) { alert("Deletion error.") }
}

const saveCdnSettings = async () => {
  try {
    await axios.post(`${window.location.origin}/api/cdn`, cdnForm.value)
    alert("CDN Node records synchronised successfully.")
  } catch { alert("Failed sync.") }
}

onMounted(() => {
  const session = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')
  if (!session || session.role !== 'admin') return router.push('/login')
  axios.defaults.headers.common['Authorization'] = `Bearer ${session.token}`
  fetchAllData()
})
</script>