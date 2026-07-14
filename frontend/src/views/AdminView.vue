<template>
  <div class="min-h-screen bg-slate-50 font-sans antialiased text-slate-800 relative">
    <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm select-none">
      <div class="flex items-center gap-4 cursor-pointer" @click="router.push('/dashboard')">
        <img src="https://bonna-website.b-cdn.net/bonnacloud-assets/BonnaCloud-Logo.png" alt="Bonna Cloud Logo" class="h-8 w-auto object-contain" />
        <h1 class="text-base font-black tracking-tight text-slate-900 border-l border-slate-200 pl-4">{{ t.controlCenter }}</h1>
      </div>
      
      <div class="flex gap-4 items-center">
        <div class="flex items-center border border-slate-200 rounded-xl px-2 py-1 bg-slate-100 text-xs font-bold shadow-xs">
          <select :value="currentLang" @change="setLanguage($event.target.value)" class="bg-transparent border-none outline-none cursor-pointer pr-1 text-slate-800 font-bold focus:ring-0 text-xs">
            <option value="tr">TR 🇹🇷</option>
            <option value="en">EN 🇬🇧</option>
          </select>
        </div>

        <div class="flex gap-2 border border-slate-200 p-0.5 bg-slate-100 rounded-xl">
          <button @click="activeTab = 'users'" :class="activeTab === 'users' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-xs transition-all">{{ t.usersControl }}</button>
          <button @click="activeTab = 'roles'" :class="activeTab === 'roles' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-xs transition-all">{{ t.rolesPermissions }}</button>
          <button @click="activeTab = 'cdn'" :class="activeTab === 'cdn' ? 'bg-white text-slate-900 font-bold shadow-sm' : 'text-slate-500 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-xs transition-all">{{ t.cdnEngine }}</button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto p-6 pb-24">
      <section v-if="activeTab === 'users'" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-base font-black text-slate-900">{{ t.userMasterList }}</h2>
            <p class="text-xs text-slate-400 font-medium mt-0.5">{{ t.manageCredentials }}</p>
          </div>
          <div class="flex gap-2">
            <button v-if="selectedUsers.length > 0" @click="deleteSelectedUsers" class="bg-red-600 hover:bg-red-500 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm active:scale-95 animate-fade-in">
              🗑️ {{ t.deleteSelected }} ({{ selectedUsers.length }})
            </button>
            
            <input type="file" ref="fileInput" @change="handleBulkUpload" accept=".xlsx" class="hidden" />
            <button @click="triggerBulkUpload" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm active:scale-95">📥 {{ t.importExcel }}</button>
            <button @click="openUserModal(null)" class="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm active:scale-95">{{ t.addNewUser }}</button>
          </div>
        </div>

        <div class="overflow-x-auto select-none">
          <table class="min-w-full text-left text-xs divide-y divide-slate-100">
            <thead>
              <tr class="text-slate-400 font-bold uppercase tracking-wider bg-slate-50/70">
                <th class="px-4 py-3 rounded-l-xl w-10 text-center">
                  <input type="checkbox" @change="toggleAllUsers" :checked="selectedUsers.length === users.length && users.length > 0" class="w-4 h-4 rounded text-blue-600 border-slate-300 focus:ring-0 cursor-pointer" />
                </th>
                <th class="px-4 py-3">{{ t.fullName }}</th>
                <th class="px-4 py-3">{{ t.company }}</th>
                <th class="px-4 py-3">{{ t.emailAddress }}</th>
                <th class="px-4 py-3">{{ t.inheritedRole }}</th>
                <th class="px-4 py-3">{{ t.status }}</th>
                <th class="px-4 py-3 rounded-r-xl w-24 text-center">{{ t.actions }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50 font-medium text-slate-700">
              <tr v-for="(user, index) in users" :key="user.id" class="hover:bg-slate-50/50 transition-colors" :class="{'bg-blue-50/40': selectedUsers.includes(user.id)}">
                <td class="px-4 py-3.5 w-10 text-center" @click.stop>
                  <input type="checkbox" :checked="selectedUsers.includes(user.id)" @click="handleUserSelect($event, user.id, index)" class="w-4 h-4 rounded text-blue-600 border-slate-300 focus:ring-0 cursor-pointer" />
                </td>
                <td class="px-4 py-3.5 font-bold text-slate-900">{{ user.name }}</td>
                <td class="px-4 py-3.5 text-slate-600">{{ user.company || '-' }}</td>
                <td class="px-4 py-3.5 text-slate-500">{{ user.email }}</td>
                <td class="px-4 py-3.5">
                  <span class="px-2.5 py-1 bg-blue-50 border border-blue-100 text-blue-700 font-bold rounded-lg">{{ user.role_name || t.noRoleAssigned }}</span>
                </td>
                <td class="px-4 py-3.5">
                  <span :class="user.isActive ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-red-50 text-red-700 border-red-100'" class="px-2 py-0.5 border rounded-md text-[10px] font-bold">{{ user.isActive ? t.active : t.blocked }}</span>
                </td>
                <td class="px-4 py-3.5 flex justify-center gap-1.5">
                  <button @click="openUserModal(user)" class="p-1.5 border border-slate-200 hover:border-slate-300 bg-white rounded-lg text-slate-600 hover:text-slate-900 shadow-sm">{{ t.edit }}</button>
                  <button @click="deleteUser(user.id)" class="p-1.5 border border-red-100 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg shadow-sm">{{ t.delete }}</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="activeTab === 'roles'" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-base font-black text-slate-900">{{ t.rolesEngineTitle }}</h2>
            <p class="text-xs text-slate-400 font-medium mt-0.5">{{ t.rolesEngineDesc }}</p>
          </div>
          <button @click="openRoleModal(null)" class="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition-all shadow-sm active:scale-95">{{ t.addNewRole }}</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="role in roles" :key="role.id" class="border border-slate-200 bg-slate-50/40 rounded-xl p-4 flex flex-col justify-between hover:shadow-md transition-all">
            <div>
              <div class="flex justify-between items-start">
                <div class="flex flex-col gap-1">
                  <h3 class="font-black text-slate-900 text-sm tracking-tight">{{ role.name }}</h3>
                  <span v-if="role.isAdmin" class="text-[9px] bg-red-600 text-white font-bold px-1.5 py-0.5 rounded-md uppercase tracking-wider w-max">Admin Yetkisi</span>
                </div>
                <span class="text-[10px] bg-slate-200 text-slate-700 font-bold px-1.5 py-0.5 rounded">ID: {{ role.id }}</span>
              </div>
              <p class="text-[10px] text-slate-400 font-bold uppercase mt-3 tracking-wider">{{ t.authorizedPaths }}</p>
              <div class="mt-1.5 space-y-1 max-h-32 overflow-y-auto pr-1">
                <div v-for="(f, i) in role.allowedFolders" :key="i" class="text-xs bg-white border border-slate-200 p-1.5 rounded-lg flex items-center justify-between shadow-sm">
                  <span class="font-bold text-slate-800 truncate max-w-[120px]" :class="f.allowed === false ? 'line-through text-red-500':''">{{ f.name }}</span>
                  <span class="text-[9px] font-bold px-1 rounded shadow-sm" :class="f.allowed === false ? 'bg-red-50 text-red-600':'bg-emerald-50 text-emerald-600'">{{ f.allowed === false ? t.excluded : t.allowed }}</span>
                </div>
                <p v-if="role.allowedFolders.length === 0" class="text-xs text-slate-400 italic">{{ t.noPermissionAssigned }}</p>
              </div>
            </div>
            <div class="flex justify-end gap-1.5 mt-5 border-t border-slate-200/60 pt-3">
              <button @click="openRoleModal(role)" class="px-3 py-1.5 text-xs font-bold border border-slate-200 hover:border-slate-300 bg-white rounded-lg shadow-sm text-slate-700">{{ t.manageRules }}</button>
              <button @click="deleteRole(role.id)" v-if="role.id !== 1" class="px-3 py-1.5 text-xs font-bold bg-red-50 text-red-600 hover:bg-red-100 border border-red-100 rounded-lg shadow-sm">{{ t.delete }}</button>
            </div>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'cdn'" class="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 max-w-xl mx-auto space-y-6">
        <div>
          <h2 class="text-base font-black text-slate-900 mb-1">{{ t.cdnConfigTitle }}</h2>
          <p class="text-xs text-slate-400 font-medium mb-6">{{ t.cdnConfigDesc }}</p>
          <form @submit.prevent="saveCdnSettings" class="space-y-4 text-xs font-bold">
            <div>
              <label class="block text-slate-600 mb-1.5">{{ t.storageZoneName }}</label>
              <input v-model="cdnForm.storageName" type="text" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
            </div>
            <div>
              <label class="block text-slate-600 mb-1.5">{{ t.storagePassword }}</label>
              <input v-model="cdnForm.storagePassword" type="password" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
            </div>
            <div>
              <label class="block text-slate-600 mb-1.5">{{ t.pullZoneUrl }}</label>
              <input v-model="cdnForm.pullZoneUrl" type="url" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
            </div>
            <div>
              <label class="block text-slate-600 mb-1.5">{{ t.regionPrefix }}</label>
              <input v-model="cdnForm.region" type="text" :placeholder="t.regionPlaceholder" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
            </div>
            <button type="submit" class="w-full bg-slate-900 hover:bg-slate-800 text-white py-2.5 rounded-xl text-xs font-bold transition-all shadow-md active:scale-95">{{ t.commitCdn }}</button>
          </form>
        </div>

        <div class="border-t border-slate-100 pt-5">
          <h3 class="text-xs font-black text-slate-900 mb-1">{{ t.searchIndexTitle }}</h3>
          <p class="text-[11px] text-slate-400 font-medium mb-3">{{ t.searchIndexDesc }}</p>
          
          <button @click="triggerManualIndex" :disabled="isIndexingStatus" class="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-300 text-white py-2.5 rounded-xl text-xs font-bold transition-all shadow-md active:scale-95 flex items-center justify-center gap-2">
            <svg v-if="isIndexingStatus" class="w-3.5 h-3.5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            {{ isIndexingStatus ? t.mappingCdn : t.runManualIndex }}
          </button>
          
          <div class="mt-3 flex items-center justify-between bg-slate-50 border border-slate-200 p-2.5 rounded-xl text-[10px] font-bold text-slate-500 uppercase tracking-wider">
            <span>{{ t.lastIndexed }} <strong class="text-slate-800">{{ lastIndexTimeDisplay }}</strong></span>
            <span>{{ t.memoryLoad }} <strong class="text-emerald-600">{{ totalIndexedItems }} objects</strong></span>
          </div>
        </div>
      </section>
    </main>

    <div v-if="showRoleModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showRoleModal = false"></div>
      <div class="relative bg-white w-full max-w-4xl rounded-2xl shadow-2xl p-6 flex flex-col z-10 text-xs font-bold h-[88vh] animate-fade-in">
        <h3 class="text-sm font-black text-slate-900 mb-3">{{ roleForm.id ? t.editRoleTitle : t.addRoleTitle }}</h3>
        
        <div class="space-y-3.5 flex-1 flex flex-col min-h-0 overflow-hidden">
          <div class="shrink-0 flex gap-4 items-end">
            <div class="flex-1">
              <label class="block text-slate-600 mb-1">{{ t.roleName }}</label>
              <input v-model="roleForm.name" type="text" :placeholder="t.roleNamePlaceholder" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
            </div>
            <div class="flex items-center gap-2 pb-2.5 select-none shrink-0 border border-slate-200 px-4 py-2 bg-slate-50 rounded-xl shadow-xs">
              <input v-model="roleForm.isAdmin" type="checkbox" id="roleAdminChk" class="w-4 h-4 text-red-600 rounded border-slate-300 focus:ring-0 cursor-pointer shadow-xs" />
              <label for="roleAdminChk" class="text-slate-800 font-black cursor-pointer text-xs">🛡️ Admin Paneli Giriş Yetkisi</label>
            </div>
          </div>
          
          <div class="shrink-0 flex flex-col">
            <label class="block text-slate-600 mb-1.5">{{ t.assignedFolders }}</label>
            <div class="border border-slate-200 rounded-xl bg-slate-50 max-h-28 overflow-y-auto p-2 space-y-1.5 shadow-inner">
              <div v-for="(folder, idx) in roleForm.allowedFolders" :key="idx" class="flex items-center justify-between bg-white border border-slate-100 p-1.5 rounded-lg shadow-sm">
                <div class="flex items-center gap-2 overflow-hidden mr-2">
                  <span class="text-xs">{{ folder.mimeType === 'application/vnd.google-apps.folder' ? '📁' : '📄' }}</span>
                  <div class="truncate">
                    <span class="font-black text-slate-800 text-[11px] block truncate" :class="folder.allowed === false ? 'line-through text-red-400':''">{{ folder.name }}</span>
                    <span class="text-[9px] font-medium text-slate-400 block truncate tracking-tight">{{ folder.id || 'Root /' }}</span>
                  </div>
                </div>
                <button type="button" @click="roleForm.allowedFolders.splice(idx, 1)" class="text-red-600 hover:text-white border border-red-200 hover:bg-red-500 hover:border-red-500 px-2.5 py-1 rounded-md text-[10px] font-black transition-all shrink-0 shadow-sm active:scale-95">{{ t.revoke }}</button>
              </div>
              <p v-if="roleForm.allowedFolders.length === 0" class="text-slate-400 font-medium italic text-center py-2.5 text-[10px]">{{ t.noActivePerms }}</p>
            </div>
          </div>

          <div class="flex items-center gap-2 bg-slate-50 border border-slate-200 p-2 rounded-xl text-xs shrink-0 select-none">
            <button v-if="adminCurrentPath" type="button" @click="adminGoToParent" class="px-2 py-1 bg-white border border-slate-300 hover:bg-slate-100 rounded-lg text-[10px] font-bold shadow-sm">▲ {{ t.up }}</button>
            <span class="text-slate-400 font-bold">{{ t.location }}</span>
            <span class="text-slate-900 font-black cursor-pointer hover:underline" @click="adminBrowseFolder('')">Home</span>
            <span v-for="(crumb, idx) in adminBreadcrumbs" :key="idx" class="flex items-center gap-1.5 text-slate-400">
              <span>/</span>
              <span class="text-slate-900 font-black cursor-pointer hover:underline truncate max-w-[120px]" @click="adminBrowseFolder(crumb.path)">{{ crumb.name }}</span>
            </span>
          </div>

          <div class="flex-1 overflow-y-auto border border-slate-100 bg-white shadow-inner rounded-xl min-h-0">
            <div v-if="loadingFolders" class="flex flex-col items-center py-12 justify-center text-slate-400">
              <div class="w-5 h-5 border-2 border-slate-300 border-t-slate-800 rounded-full animate-spin mb-2"></div>
              <p class="text-[10px] font-medium">Opening cloud folder layer...</p>
            </div>

            <table class="min-w-full divide-y divide-slate-100 text-left text-sm" v-else>
              <thead>
                <tr class="text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-50/70 select-none">
                  <th scope="col" class="pl-4 py-2 w-8 rounded-l-xl">{{ t.select }}</th>
                  <th scope="col" class="pl-3 py-2">{{ t.fileName }}</th>
                  <th scope="col" class="px-3 py-2 w-24">{{ t.size }}</th>
                  <th scope="col" class="px-3 py-2 w-24 rounded-r-xl">{{ t.type }}</th>
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
                    {{ item.mimeType === 'application/vnd.google-apps.folder' ? t.folder : getExtension(item.name) }}
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="adminItems.length === 0 && !loadingFolders" class="text-slate-400 italic text-center py-12 text-xs">{{ t.emptyDir }}</div>
          </div>
        </div>
        
        <div class="flex justify-end gap-2 mt-3 border-t border-slate-100 pt-3 shrink-0">
          <button @click="showRoleModal = false" class="px-4 py-2 border border-slate-200 bg-white rounded-xl text-slate-700">{{ t.cancel }}</button>
          <button @click="saveRole" class="px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl">{{ t.commitChanges }}</button>
        </div>
      </div>
    </div>

    <div v-if="showUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="showUserModal = false"></div>
      <div class="relative bg-white w-full max-w-md rounded-2xl shadow-2xl p-6 z-10 text-xs font-bold">
        <h3 class="text-sm font-black text-slate-900 mb-4">{{ userForm.id ? t.editUserTitle : t.newUserTitle }}</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-slate-600 mb-1.5">{{ t.userFullName }}</label>
            <input v-model="userForm.name" type="text" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">{{ t.emailAddress }}</label>
            <input v-model="userForm.email" type="email" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div>
            <label class="block text-slate-600 mb-1.5">{{ t.passwordLabel }} {{ userForm.id ? t.passwordKeep : '' }}</label>
            <input v-model="userForm.password" type="password" :required="!userForm.id" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-slate-600 mb-1.5">{{ t.companyOrganization }}</label>
              <input v-model="userForm.company" type="text" :placeholder="t.companyPlaceholder" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-medium focus:outline-none focus:border-slate-900 focus:bg-white" />
            </div>
            <div>
              <label class="block text-slate-600 mb-1.5">{{ t.assignAccessRole }}</label>
              <select v-model="userForm.role_id" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 font-bold text-blue-700 focus:outline-none focus:border-slate-900 focus:bg-white">
                <option :value="null">{{ t.noRoleAccessDenied }}</option>
                <option v-for="r in roles" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>
          </div>
          <div class="flex items-center gap-2 pt-2">
            <input v-model="userForm.isActive" type="checkbox" id="userActiveChk" class="w-4 h-4 text-slate-900 rounded border-slate-300" />
            <label for="userActiveChk" class="text-slate-700 cursor-pointer select-none">{{ t.authorizeUserCheck }}</label>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6 border-t border-slate-100 pt-4">
          <button @click="showUserModal = false" class="px-4 py-2 border border-slate-200 bg-white rounded-xl text-slate-700">{{ t.cancel }}</button>
          <button @click="saveUser" class="px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl">{{ t.commitCredentials }}</button>
        </div>
      </div>
    </div>

    <div v-if="confirmDialog.isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 select-none">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm" @click="cancelConfirm"></div>
      <div class="relative bg-white w-full max-w-sm rounded-3xl shadow-2xl p-6 z-10 text-center animate-fade-in border border-slate-100">
        <div class="mx-auto flex items-center justify-center h-14 w-14 rounded-full mb-4 shadow-inner bg-amber-50 text-amber-500 border border-amber-100">
          <svg class="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        </div>
        <h3 class="text-lg font-black text-slate-900 mb-2">{{ confirmDialog.title }}</h3>
        <p class="text-sm text-slate-500 font-medium mb-8 leading-relaxed">{{ confirmDialog.message }}</p>
        <div class="flex gap-3 justify-center w-full">
          <button @click="cancelConfirm" class="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 hover:bg-slate-100 text-slate-700 text-xs font-black uppercase tracking-wider rounded-xl transition-all shadow-sm active:scale-95">{{ t.no }}</button>
          <button @click="acceptConfirm" class="flex-1 px-4 py-3 bg-amber-500 hover:bg-amber-600 text-white text-xs font-black uppercase tracking-wider rounded-xl transition-all shadow-md active:scale-95">{{ t.yes }}</button>
        </div>
      </div>
    </div>

    <div v-if="toast.show" class="fixed bottom-10 left-1/2 transform -translate-x-1/2 px-5 py-3 rounded-xl shadow-2xl font-bold text-xs z-[150] flex items-center gap-2 border animate-fade-in transition-all" :class="toast.type === 'success' ? 'bg-emerald-500 text-white border-emerald-400' : 'bg-red-500 text-white border-red-400'">
      <svg v-if="toast.type === 'success'" class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
      <svg v-else class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
      {{ toast.message }}
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { currentLang, setLanguage, t } from '../utils/i18n.js'

const router = useRouter()
const activeTab = ref("users")

const users = ref([])
const roles = ref([])
const adminItems = ref([]) 
const adminCurrentPath = ref("") 
const loadingFolders = ref(false)

const showUserModal = ref(false)
const showRoleModal = ref(false)

const fileInput = ref(null)

const selectedUsers = ref([])
const lastSelectedIndex = ref(null)

const cdnForm = ref({ storageName: "", storagePassword: "", pullZoneUrl: "", region: "" })
const userForm = ref({ id: null, name: "", email: "", password: "", role_id: null, company: "", isActive: true })
const roleForm = ref({ id: null, name: "", allowedFolders: [], isAdmin: false })

const isIndexingStatus = ref(false)
const lastIndexTimeDisplay = ref("Never")
const totalIndexedItems = ref(0)
let pollingInterval = null

const toast = ref({ show: false, message: '', type: 'success' })
let toastTimer = null

const triggerToast = (msg, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { show: true, message: msg, type }
  toastTimer = setTimeout(() => { toast.value.show = false }, 4000)
}

const confirmDialog = ref({ isOpen: false, title: '', message: '', resolvePromise: null })

const showConfirm = (title, message) => {
  return new Promise((resolve) => {
    confirmDialog.value = { isOpen: true, title, message, resolvePromise: resolve }
  })
}

const acceptConfirm = () => {
  confirmDialog.value.isOpen = false
  if (confirmDialog.value.resolvePromise) confirmDialog.value.resolvePromise(true)
}

const cancelConfirm = () => {
  confirmDialog.value.isOpen = false
  if (confirmDialog.value.resolvePromise) confirmDialog.value.resolvePromise(false)
}

const fetchIndexStatus = async () => {
  try {
    const resp = await axios.get(`${window.location.origin}/api/cdn/index-status`)
    isIndexingStatus.value = resp.data.is_indexing
    totalIndexedItems.value = resp.data.total_items
    lastIndexTimeDisplay.value = resp.data.last_index_time ? new Date(resp.data.last_index_time).toLocaleString() : "Never"
  } catch (err) {
    console.error("Index status sync failure:", err)
  }
}

const triggerManualIndex = async () => {
  isIndexingStatus.value = true
  try {
    await axios.post(`${window.location.origin}/api/cdn/index`)
    triggerToast(t.value.mappingCdn, "success")
    startStatusPolling()
  } catch (err) {
    triggerToast("Failed to initiate secure indexing node.", "error")
    isIndexingStatus.value = false
  }
}

const startStatusPolling = () => {
  if (pollingInterval) clearInterval(pollingInterval)
  pollingInterval = setInterval(async () => {
    await fetchIndexStatus()
    if (!isIndexingStatus.value) {
      clearInterval(pollingInterval)
      triggerToast(t.value.indexCompiled, "success")
    }
  }, 3000)
}

const fetchAllData = async () => {
  try {
    const uResp = await axios.get(`${window.location.origin}/api/users`)
    users.value = uResp.data
    const rResp = await axios.get(`${window.location.origin}/api/roles`)
    roles.value = rResp.data
    const cResp = await axios.get(`${window.location.origin}/api/cdn`)
    cdnForm.value = cResp.data
    await fetchIndexStatus()
  } catch (err) {
    triggerToast("Authorization node sync error.", "error")
  }
}

const handleUserSelect = (event, userId, index) => {
  const isChecked = event.target.checked
  if (event.shiftKey && lastSelectedIndex.value !== null) {
    const start = Math.min(index, lastSelectedIndex.value)
    const end = Math.max(index, lastSelectedIndex.value)
    const idsInRange = users.value.slice(start, end + 1).map(u => u.id)
    if (isChecked) {
      const newSet = new Set([...selectedUsers.value, ...idsInRange])
      selectedUsers.value = Array.from(newSet)
    } else {
      selectedUsers.value = selectedUsers.value.filter(id => !idsInRange.includes(id))
    }
  } else {
    if (isChecked) {
      selectedUsers.value.push(userId)
    } else {
      selectedUsers.value = selectedUsers.value.filter(id => id !== userId)
    }
  }
  lastSelectedIndex.value = index
}

const toggleAllUsers = (event) => {
  if (event.target.checked) {
    selectedUsers.value = users.value.map(u => u.id)
  } else {
    selectedUsers.value = []
  }
  lastSelectedIndex.value = null
}

const deleteSelectedUsers = async () => {
  if (selectedUsers.value.length === 0) return
  const isConfirmed = await showConfirm(t.value.bulkDeleteTitle, t.value.bulkDeleteConfirm)
  if (!isConfirmed) return
  
  const session = JSON.parse(localStorage.getItem('bonna_user_session') || '{}')
  const currentUserId = session.id
  let errorOccurred = false
  let deletedCount = 0

  for (const id of selectedUsers.value) {
    if (id === currentUserId) {
      triggerToast(t.value.ownAccountError, "error")
      continue
    }
    try {
      await axios.delete(`${window.location.origin}/api/users/${id}`)
      deletedCount++
    } catch (err) { errorOccurred = true }
  }
  
  if (errorOccurred) triggerToast("Error occurred while deleting some users.", "error")
  else if (deletedCount > 0) triggerToast(t.value.userSaved, "success")
  
  selectedUsers.value = [] 
  lastSelectedIndex.value = null
  fetchAllData() 
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
    if (parentFound) return parentFound.allowed === true
  }
  return false
}

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
    roleForm.value.allowedFolders.push({ id: item.id, name: item.name, mimeType: item.mimeType, size: item.size || 0, allowed: newState })
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
    roleForm.value = { id: role.id, name: role.name, allowedFolders: JSON.parse(JSON.stringify(role.allowedFolders)), isAdmin: role.isAdmin || false }
  } else {
    roleForm.value = { id: null, name: "", allowedFolders: [], isAdmin: false }
  }
  showRoleModal.value = true
  await adminBrowseFolder("") 
}

const saveRole = async () => {
  if (!roleForm.value.name.trim()) return triggerToast(t.value.roleRequired, 'error')
  try {
    if (roleForm.value.id) {
      await axios.put(`${window.location.origin}/api/roles/${roleForm.value.id}`, roleForm.value)
    } else {
      await axios.post(`${window.location.origin}/api/roles`, roleForm.value)
    }
    showRoleModal.value = false
    fetchAllData()
    triggerToast(t.value.roleSaved, "success")
  } catch (err) { triggerToast(err.response?.data?.detail || "Role save failed.", "error") }
}

const deleteRole = async (id) => {
  const isConfirmed = await showConfirm(t.value.purgeRoleTitle, t.value.purgeRoleConfirm)
  if (!isConfirmed) return
  try {
    await axios.delete(`${window.location.origin}/api/roles/${id}`)
    fetchAllData()
    triggerToast(t.value.roleSaved, "success")
  } catch (err) { triggerToast('Purge aborted due to system error.', "error") }
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
    userForm.value = { id: user.id, name: user.name, email: user.email, password: "", role_id: user.role_id, company: user.company, isActive: user.isActive }
  } else {
    userForm.value = { id: null, name: "", email: "", password: "", role_id: roles.value[0]?.id || null, company: "", isActive: true }
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
    triggerToast(t.value.userSaved, "success")
  } catch (err) { triggerToast(err.response?.data?.detail || "Credential modification error.", "error") }
}

const deleteUser = async (id) => {
  const isConfirmed = await showConfirm(t.value.deleteUserTitle, t.value.deleteUserConfirm)
  if (!isConfirmed) return
  try {
    await axios.delete(`${window.location.origin}/api/users/${id}`)
    fetchAllData()
    triggerToast(t.value.userSaved, "success")
  } catch (err) { triggerToast("Deletion error. Action could not be completed.", "error") }
}

const triggerBulkUpload = () => fileInput.value.click()

const handleBulkUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const isConfirmed = await showConfirm(t.value.excelImportTitle, `"${file.name}" ${t.value.excelImportConfirm}`)
  if (!isConfirmed) { event.target.value = ''; return }
  
  const formData = new FormData()
  formData.append("file", file)
  try {
    const resp = await axios.post(`${window.location.origin}/api/users/bulk`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    triggerToast(resp.data.message, "success")
    fetchAllData() 
  } catch (err) {
    triggerToast(err.response?.data?.detail || err.message, "error")
  } finally { event.target.value = '' }
}

const saveCdnSettings = async () => {
  try {
    await axios.post(`${window.location.origin}/api/cdn`, cdnForm.value)
    triggerToast(t.value.cdnSynced, "success")
    startStatusPolling()
  } catch { triggerToast("Failed to sync CDN configurations.", "error") }
}

onMounted(() => {
  const session = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')
  if (!session || session.role !== 'admin') return router.push('/login')
  axios.defaults.headers.common['Authorization'] = `Bearer ${session.token}`
  fetchAllData()
})

onUnmounted(() => { if (pollingInterval) clearInterval(pollingInterval) })
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>