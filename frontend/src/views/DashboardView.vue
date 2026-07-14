<template>
  <div class="min-h-screen bg-white font-sans text-slate-800 relative pb-4">
    
    <header class="flex flex-wrap items-center justify-between px-4 sm:px-6 lg:px-12 py-3 lg:py-4 bg-white select-none gap-y-3">
      <div class="flex items-center cursor-pointer shrink-0" @click="goToRoot">
        <img src="https://bonna-website.b-cdn.net/bonnacloud-assets/BonnaCloud-Logo.png" alt="Bonna Cloud Logo" class="h-7 sm:h-9 w-auto object-contain" />
      </div>

      <div class="w-full lg:w-auto lg:flex-1 max-w-xl relative order-3 lg:order-2 lg:mx-8">
        <input v-model="searchQuery" type="text" :placeholder="t.searchPlaceholder" class="w-full bg-transparent border-b border-slate-300 text-sm sm:text-base font-normal text-slate-800 placeholder-slate-400 pb-1.5 pr-8 focus:outline-none focus:border-slate-900 transition-colors rounded-none" />
        <div class="absolute right-2 bottom-2 text-slate-900 pointer-events-none">
          <svg class="h-4 w-4 sm:h-5 sm:w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
      </div>

      <div class="flex items-center gap-2 sm:gap-4 shrink-0 order-2 lg:order-3">
        <div class="flex items-center border border-slate-200 rounded-xl px-2 py-1.5 bg-slate-50 text-xs font-bold shadow-sm">
          <select :value="currentLang" @change="setLanguage($event.target.value)" class="bg-transparent border-none outline-none cursor-pointer pr-1 text-slate-800 font-bold focus:ring-0 text-xs">
            <option value="tr">TR</option>
            <option value="en">EN</option>
          </select>
        </div>

        <button v-if="userSession?.role === 'admin'" @click="router.push('/admin')" class="flex items-center gap-1 sm:gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-900 border border-slate-200 hover:border-slate-300 bg-slate-50 hover:bg-white px-2 py-1.5 sm:px-2.5 sm:py-1.5 rounded-xl transition-all shadow-sm active:scale-95">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          <span class="hidden sm:inline">{{ t.adminPanel }}</span>
          <span class="inline sm:hidden">Admin</span>
        </button>

        <div v-if="userSession?.role === 'admin'" class="h-5 w-px bg-slate-200 hidden sm:block"></div>

        <div v-if="userSession" class="text-right hidden sm:block">
          <div class="text-xs font-bold text-slate-800">{{ userSession.name }}</div>
          <div class="text-[10px] text-slate-500 font-medium uppercase tracking-wider">{{ userSession.role_name || userSession.role }}</div>
        </div>

        <button @click="handleLogout" class="flex items-center gap-1.5 text-xs font-bold text-red-600 hover:text-red-700 border border-red-100 hover:border-red-200 bg-red-50 hover:bg-red-100 px-2.5 sm:px-3 py-1.5 rounded-xl transition-all shadow-sm active:scale-95">
          <svg class="w-3.5 h-3.5 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          <span class="hidden sm:inline">{{ t.logout }}</span>
        </button>
      </div>
    </header>

    <hr class="border-slate-200" />

    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between px-4 sm:px-6 lg:px-12 py-3 bg-white select-none gap-3">
      <div class="flex items-center gap-2 w-full sm:w-auto overflow-x-auto whitespace-nowrap pb-1 sm:pb-0 scrollbar-hide">
        <button v-if="currentPath" @click="goToParentFolder" class="p-1 sm:p-1.5 shrink-0 text-slate-500 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200/80 rounded-lg transition-all active:scale-90" title="Go to parent folder">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
        </button>

        <nav class="flex items-center space-x-1.5 text-xs sm:text-sm font-normal text-slate-600">
          <span class="cursor-pointer hover:text-slate-950 transition-colors" @click="goToRoot">{{ t.home }}</span>
          <template v-for="(crumb, index) in breadcrumbs" :key="index">
            <span class="text-slate-300">/</span>
            <span :class="crumb.isSearch ? 'text-slate-900 font-bold' : 'cursor-pointer hover:text-slate-950 transition-colors'" @click="!crumb.isSearch ? fetchFiles(crumb.path) : null" class="max-w-[120px] sm:max-w-[200px] truncate">{{ crumb.name }}</span>
          </template>
        </nav>
      </div>

      <div class="flex items-center justify-between w-full sm:w-auto gap-3 shrink-0">
        <div class="flex items-center gap-1 border border-slate-200 rounded-lg px-2 py-1 bg-slate-50/50 shadow-sm text-xs font-bold text-slate-700">
          <span class="text-slate-400 font-medium select-none hidden sm:inline">{{ t.sortBy }}</span>
          <select v-model="sortBy" class="bg-transparent border-none outline-none cursor-pointer pr-1 text-slate-800 font-bold focus:ring-0 text-xs">
            <option value="name">{{ t.name }}</option>
            <option value="size">{{ t.size }}</option>
          </select>
          <button @click="toggleSortOrder" class="text-slate-400 hover:text-slate-900 transition-colors pl-1 border-l border-slate-200 active:scale-90" title="Toggle Sort Order">
            <svg v-if="sortOrder === 'asc'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"/></svg>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/></svg>
          </button>
        </div>

        <div class="flex items-center border border-slate-300 rounded-full p-0.5 bg-white overflow-hidden shadow-sm">
          <button @click="viewMode = 'list'" :class="viewMode === 'list' ? 'bg-slate-200 text-slate-900 font-bold' : 'text-slate-400 hover:text-slate-600'" class="px-2 py-1 rounded-full transition-all">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
          <button @click="viewMode = 'grid'" :class="viewMode === 'grid' ? 'bg-slate-200 text-slate-900 font-bold' : 'text-slate-400 hover:text-slate-600'" class="px-2 py-1 rounded-full transition-all">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
          </button>
        </div>
      </div>
    </div>

    <main class="px-4 sm:px-6 lg:px-12 py-3 sm:py-4 min-h-[60vh]" :class="{'pb-24': selectedItems.length > 0}">
      <div v-if="loading" class="flex flex-col items-center justify-center h-64 text-slate-800">
        <div class="w-8 h-8 border-2 border-slate-200 border-t-slate-800 rounded-full animate-spin mb-4"></div>
      </div>

      <div v-else-if="systemMessage" class="flex flex-col items-center justify-center h-64 px-4">
        <div class="bg-amber-50 text-amber-700 p-5 rounded-xl border border-amber-100 max-w-lg text-center text-sm font-medium">{{ systemMessage }}</div>
      </div>

      <div v-else-if="displayItems.length === 0" class="flex flex-col items-center justify-center h-64 text-slate-400 px-4 text-center">
        <p class="text-sm font-medium">{{ t.noFiles }}</p>
      </div>

      <template v-else>
        <div v-if="viewMode === 'grid' && downloadableItems.length > 0" class="flex justify-between items-center mb-3 px-1">
          <button @click="toggleSelectAll" class="flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-slate-900 transition-colors group">
            <div class="w-4 h-4 rounded border border-slate-300 bg-white flex items-center justify-center" :class="{'bg-theme-primary border-theme-primary': isAllSelected}">
              <svg v-if="isAllSelected" class="w-3 h-3 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
            </div>
            {{ t.selectAll }}
          </button>
        </div>

        <div v-if="viewMode === 'grid'" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-8 gap-3 sm:gap-4">
          <div v-for="item in displayItems" :key="item.id" @click="handleItemClick(item)" :class="{'ring-2 ring-theme-primary bg-slate-50': isSelected(item)}" class="group bg-slate-50/40 hover:bg-slate-50 border border-transparent hover:border-slate-200 rounded-xl p-2.5 cursor-pointer hover:shadow-md transition-all duration-300 flex flex-col items-center justify-between text-center min-h-[120px] sm:min-h-[145px] relative">
            
            <div v-if="item.mimeType !== 'application/vnd.google-apps.folder'" 
                 :class="selectedItems.length > 0 ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'"
                 class="absolute top-1.5 left-1.5 z-10 transition-opacity duration-200">
              <div @click.stop="toggleSelection(item)" class="w-4 h-4 rounded border border-slate-300 bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-sm" :class="{'bg-theme-primary border-theme-primary': isSelected(item)}">
                <svg v-if="isSelected(item)" class="w-3 h-3 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
              </div>
            </div>

            <div v-if="item.mimeType !== 'application/vnd.google-apps.folder'" 
                 :class="activeDropdownId === item.id ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'"
                 class="absolute top-1.5 right-1.5 z-20 transition-opacity duration-200" @click.stop>
              <button @click.stop="toggleDropdown(item.id)" class="w-5 h-5 flex items-center justify-center text-slate-400 hover:text-slate-900 bg-white border border-slate-200 hover:border-slate-300 rounded-md shadow-sm transition-colors bg-white/90 backdrop-blur-sm">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>
              </button>
              
              <div v-if="activeDropdownId === item.id" class="absolute right-0 top-6 bg-white border border-slate-200 rounded-lg shadow-xl z-50 py-1 w-28 sm:w-32 text-left animate-fade-in">
                <button @click.stop="shareItem(item); activeDropdownId = null" class="w-full px-3 py-1.5 text-[11px] font-bold text-slate-700 hover:bg-slate-50 flex items-center gap-1.5 transition-colors">
                  <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                  {{ t.share }}
                </button>
                <button @click.stop="downloadItem(item); activeDropdownId = null" :disabled="downloadingItemId === item.id" class="w-full px-3 py-1.5 text-[11px] font-bold text-slate-700 hover:bg-slate-50 flex items-center gap-1.5 transition-colors disabled:opacity-50">
                  <svg v-if="downloadingItemId === item.id" class="w-3 h-3 animate-spin text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                  <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                  {{ t.download }}
                </button>
              </div>
            </div>

            <div class="w-full aspect-square bg-white rounded-lg border border-slate-100 mb-1.5 flex items-center justify-center overflow-hidden relative shadow-sm group/media select-none">
              <svg v-if="item.mimeType === 'application/vnd.google-apps.folder'" class="w-8 h-8 sm:w-11 sm:h-11 text-theme-primary fill-current" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
              
              <img v-else-if="isImage(item.name)" :src="getPreviewUrl(item, 'grid')" class="w-full h-full object-cover" loading="lazy" />
              
              <div v-else-if="isVideo(item.name)" class="w-full h-full relative flex items-center justify-center bg-slate-100">
                <video :src="getPreviewUrl(item, 'grid')" class="w-full h-full object-cover" preload="metadata" muted playsinline></video>
                <div class="absolute inset-0 bg-slate-900/10 group-hover/media:bg-slate-900/30 transition-colors flex items-center justify-center">
                  <svg class="w-6 h-6 sm:w-8 sm:h-8 text-white drop-shadow-lg opacity-90 group-hover/media:opacity-100 group-hover/media:scale-110 transition-all" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                </div>
              </div>

              <svg v-else-if="isWord(item.name)" class="w-10 h-10 sm:w-14 sm:h-14" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                <path d="M240 60V110H290L240 60Z" fill="black"/>
                <rect x="70" y="190" width="260" height="85" fill="#345a9a"/>
                <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">DOCX</text>
              </svg>

              <svg v-else-if="isExcel(item.name)" class="w-10 h-10 sm:w-14 sm:h-14" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                <path d="M240 60V110H290L240 60Z" fill="black"/>
                <rect x="70" y="190" width="260" height="85" fill="#137e43"/>
                <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">XLSX</text>
              </svg>

              <svg v-else-if="isPPTX(item.name)" class="w-10 h-10 sm:w-14 sm:h-14" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                <path d="M240 60V110H290L240 60Z" fill="black"/>
                <rect x="70" y="190" width="260" height="85" fill="#d24715"/>
                <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">PPTX</text>
              </svg>

              <svg v-else-if="isPDF(item.name)" class="w-10 h-10 sm:w-14 sm:h-14" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                <path d="M240 60V110H290L240 60Z" fill="black"/>
                <rect x="70" y="190" width="260" height="85" fill="#c42b2b"/>
                <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">PDF</text>
              </svg>

              <div class="w-full h-full flex flex-col items-center justify-center text-slate-400 bg-slate-50/50 rounded-lg p-1.5" v-else>
                <svg class="w-5 h-5 opacity-60 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                <span class="text-[7px] font-bold uppercase tracking-wider text-slate-400">{{ getExtension(item.name) }}</span>
              </div>
            </div>
            
            <div class="w-full">
              <h3 class="text-[10px] sm:text-[11px] font-bold text-slate-700 truncate px-0.5 group-hover:text-blue-600 transition-colors">{{ item.name }}</h3>
              <p v-if="item.mimeType !== 'application/vnd.google-apps.folder'" class="text-[8px] sm:text-[9px] text-slate-400 mt-0.5 font-bold tracking-wider uppercase">
                {{ formatSize(item.size) }}
              </p>
              <p class="text-[8px] sm:text-[9px] text-slate-400 mt-0.5 font-bold uppercase tracking-wider" v-else>{{ t.folder }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="viewMode === 'list'" class="overflow-x-auto border border-slate-100 rounded-xl sm:border-none sm:rounded-none">
          <table class="min-w-full divide-y divide-slate-100 text-left text-sm">
            <thead>
              <tr class="text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-50/70">
                <th scope="col" class="pl-4 py-2 w-8 rounded-l-xl">
                  <div @click="toggleSelectAll" class="w-3.5 h-3.5 rounded border border-slate-300 bg-white flex items-center justify-center cursor-pointer" :class="{'bg-theme-primary border-theme-primary': isAllSelected && downloadableItems.length > 0}">
                    <svg v-if="isAllSelected" class="w-2.5 h-2.5 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                </th>
                
                <th scope="col" class="pl-2 pr-4 py-2 cursor-pointer select-none hover:text-slate-600 group" @click="handleSort('name')">
                  <div class="flex items-center gap-1">
                    {{ t.fileName }}
                    <span :class="sortBy === 'name' ? 'text-slate-800' : 'text-slate-300 group-hover:text-slate-400 transition-colors'">
                      <svg v-if="sortBy === 'name' && sortOrder === 'asc'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/></svg>
                    </span>
                  </div>
                </th>

                <th scope="col" class="px-3 py-2 w-24 cursor-pointer select-none hover:text-slate-600 group hidden sm:table-cell" @click="handleSort('size')">
                  <div class="flex items-center gap-1">
                    {{ t.size }}
                    <span :class="sortBy === 'size' ? 'text-slate-800' : 'text-slate-300 group-hover:text-slate-400 transition-colors'">
                      <svg v-if="sortBy === 'size' && sortOrder === 'asc'" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/></svg>
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/></svg>
                    </span>
                  </div>
                </th>
                
                <th scope="col" class="px-3 py-2 w-24 hidden md:table-cell">{{ t.type }}</th> 
                <th scope="col" class="px-2 py-2 w-14 text-center">{{ t.share }}</th>
                <th scope="col" class="px-2 py-2 w-14 rounded-r-xl text-center">{{ t.download }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="item in displayItems" :key="item.id" @click="handleItemClick(item)" :class="{'bg-slate-50': isSelected(item)}" class="hover:bg-slate-50/70 cursor-pointer group">
                <td class="pl-4 sm:pl-5 pr-0 py-1.5" @click.stop="item.mimeType !== 'application/vnd.google-apps.folder' ? toggleSelection(item) : null">
                  <div v-if="item.mimeType !== 'application/vnd.google-apps.folder'" class="w-3.5 h-3.5 rounded border border-slate-300 bg-white flex items-center justify-center" :class="{'bg-theme-primary border-theme-primary': isSelected(item)}">
                    <svg v-if="isSelected(item)" class="w-2.5 h-2.5 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                </td>
                <td class="pl-2 pr-4 py-1.5 font-semibold text-slate-700 whitespace-nowrap flex items-center gap-2.5 sm:gap-3">
                  <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-md overflow-hidden flex items-center justify-center shrink-0 border border-slate-100 bg-white relative">
                    <svg class="w-4 h-4 sm:w-5 sm:h-5 text-theme-primary fill-current" viewBox="0 0 24 24"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                    <img v-if="isImage(item.name)" :src="getPreviewUrl(item, 'list')" class="w-full h-full object-cover" />
                    
                    <div v-else-if="isVideo(item.name)" class="w-full h-full relative flex items-center justify-center bg-slate-100">
                      <video :src="getPreviewUrl(item, 'list')" class="w-full h-full object-cover" preload="metadata" muted playsinline></video>
                      <div class="absolute inset-0 bg-slate-900/20 flex items-center justify-center">
                        <svg class="w-3 h-3 text-white drop-shadow-sm" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                      </div>
                    </div>

                    <svg v-else-if="isWord(item.name)" class="w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                      <path d="M240 60V110H290L240 60Z" fill="black"/>
                      <rect x="70" y="190" width="260" height="85" fill="#345a9a"/>
                      <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">DOCX</text>
                    </svg>

                    <svg v-else-if="isExcel(item.name)" class="w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                      <path d="M240 60V110H290L240 60Z" fill="black"/>
                      <rect x="70" y="190" width="260" height="85" fill="#137e43"/>
                      <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">XLSX</text>
                    </svg>

                    <svg v-else-if="isPPTX(item.name)" class="w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                      <path d="M240 60V110H290L240 60Z" fill="black"/>
                      <rect x="70" y="190" width="260" height="85" fill="#d24715"/>
                      <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">PPTX</text>
                    </svg>

                    <svg v-else-if="isPDF(item.name)" class="w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M110 60H240L290 110V340H110V60Z" fill="white" stroke="black" stroke-width="24" stroke-linejoin="miter"/>
                      <path d="M240 60V110H290L240 60Z" fill="black"/>
                      <rect x="70" y="190" width="260" height="85" fill="#c42b2b"/>
                      <text x="200" y="250" font-family="system-ui, -apple-system, sans-serif" font-weight="normal" font-size="46" fill="white" text-anchor="middle" letter-spacing="0.5">PDF</text>
                    </svg>

                    <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                  </div>
                  <div class="flex flex-col">
                     <span class="truncate text-[11px] sm:text-xs font-bold text-slate-800 max-w-[150px] sm:max-w-md group-hover:text-blue-600 transition-colors">{{ item.name }}</span>
                     <span v-if="item.mimeType !== 'application/vnd.google-apps.folder'" class="text-[9px] text-slate-400 sm:hidden mt-0.5">{{ formatSize(item.size) }}</span>
                  </div>
                </td>
                <td class="px-3 py-1.5 text-slate-500 text-xs font-bold hidden sm:table-cell">{{ item.mimeType === 'application/vnd.google-apps.folder' ? '--' : formatSize(item.size) }}</td>
                <td class="px-3 py-1.5 text-slate-400 text-xs font-bold uppercase hidden md:table-cell">{{ item.mimeType === 'application/vnd.google-apps.folder' ? t.folder : getExtension(item.name) }}</td>
                <td class="px-2 py-1.5 text-center">
                  <button v-if="item.mimeType !== 'application/vnd.google-apps.folder'" @click.stop="shareItem(item)" class="inline-flex items-center justify-center p-1 text-slate-400 hover:text-slate-900 bg-white border border-slate-200 rounded-md shadow-sm">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                  </button>
                </td>
                <td class="px-2 py-1.5 text-center">
                  <button v-if="item.mimeType !== 'application/vnd.google-apps.folder'" @click.stop="downloadItem(item)" :disabled="downloadingItemId === item.id" class="inline-flex items-center justify-center p-1 bg-white border border-slate-200 rounded-md shadow-sm">
                    <svg v-if="downloadingItemId === item.id" class="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2a8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                    <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </main>

    <div v-if="selectedItems.length > 0" class="fixed bottom-0 inset-x-0 z-40 flex flex-col sm:flex-row items-center justify-between px-6 sm:px-12 py-3 bg-theme-primary text-slate-900 select-none shadow-[0_-10px_40px_rgba(0,0,0,0.1)] rounded-t-2xl border-t border-yellow-600/20 gap-2 sm:gap-0">
      <div class="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-start">
        <span class="font-black text-sm sm:text-base">{{ selectedItems.length }} {{ t.filesSelected }}</span>
        <button @click="clearSelection" class="w-7 h-7 flex items-center justify-center bg-black/10 hover:bg-black/20 rounded-full text-xs">✕</button>
      </div>
      <button @click="downloadSelected" :disabled="isDownloading" class="w-full sm:w-auto flex items-center justify-center gap-2 bg-slate-900 text-white px-6 py-2.5 rounded-xl text-xs font-bold hover:bg-slate-800 transition-all shadow-lg sm:shadow-none">
        <svg v-if="isDownloading" class="w-3.5 h-3.5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        {{ isDownloading ? t.preparingZip : t.downloadSelected }}
      </button>
    </div>

    <div v-if="selectedFile" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 select-none pl-[calc(env(safe-area-inset-left)+12px)] pr-[calc(env(safe-area-inset-right)+12px)] pt-[calc(env(safe-area-inset-top)+12px)] pb-[calc(env(safe-area-inset-bottom)+12px)]">
      <div class="absolute inset-0 bg-slate-900/95 backdrop-blur-xs" @click="selectedFile = null"></div>
      
      <div class="relative bg-white w-full max-w-5xl h-auto max-h-[78dvh] sm:max-h-[85vh] rounded-2xl sm:rounded-3xl overflow-hidden shadow-2xl flex flex-col z-10 animate-fade-in border border-slate-200/50">
        
        <div class="p-3 border-b border-slate-100 flex justify-between items-center bg-slate-50 shrink-0 min-h-[52px]">
          <div class="overflow-hidden pr-2">
            <h3 class="font-bold text-slate-800 text-[11px] sm:text-sm truncate max-w-[120px] sm:max-w-xl">{{ selectedFile.name }}</h3>
            <p class="text-[9px] sm:text-[11px] text-slate-500 mt-0.5 font-bold uppercase tracking-wider">
              {{ formatSize(selectedFile.size) }} • {{ getExtension(selectedFile.name) }}
            </p>
          </div>
          
          <div class="flex items-center gap-1.5 shrink-0">
            <button @click="shareItem(selectedFile)" class="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 border border-slate-200 bg-white rounded-xl transition-all shadow-sm active:scale-95">
              <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
              <span class="hidden sm:inline">{{ t.share }}</span>
            </button>
            
            <button @click="downloadItem(selectedFile)" :disabled="downloadingItemId === selectedFile.id" class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-black text-slate-900 bg-theme-primary border border-yellow-600/10 rounded-xl transition-all shadow-sm active:scale-95 disabled:opacity-50 hover:brightness-95">
              <svg v-if="downloadingItemId === selectedFile.id" class="w-3.5 h-3.5 animate-spin text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              <svg class="w-3.5 h-3.5 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24" v-else><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
              <span class="hidden sm:inline">{{ t.download }}</span>
            </button>
            <div class="h-4 w-px bg-slate-200 mx-0.5"></div>
            <button @click="selectedFile = null" class="w-7 h-7 flex items-center justify-center hover:bg-slate-200 rounded-full text-slate-500 transition-colors text-xs font-bold">✕</button>
          </div>
        </div>

        <div class="flex-1 bg-slate-100/50 flex items-center justify-center p-3 relative touch-pan-y min-h-0 overflow-hidden" 
             @touchstart="handleTouchStart" 
             @touchend="handleTouchEnd">
             
          <button v-if="hasPrevFile" @click.stop="prevFile" class="absolute left-2 z-30 w-9 h-9 flex items-center justify-center bg-white/80 hover:bg-white text-slate-800 rounded-full shadow-lg transition-all active:scale-90 border border-slate-200/50 backdrop-blur-sm hidden sm:flex">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
          </button>

          <div class="w-full h-full flex items-center justify-center max-h-[calc(78dvh-60px)] sm:max-h-[calc(85vh-60px)]"
               :class="isPDF(selectedFile.name) ? 'overflow-y-auto pointer-events-auto' : 'overflow-hidden pointer-events-none sm:pointer-events-auto'">
            <img v-if="isImage(selectedFile.name)" :src="previewUrl" class="max-w-full max-h-full object-contain select-none pointer-events-none rounded-lg" />
            <video v-else-if="isVideo(selectedFile.name)" :src="previewUrl" controls autoplay muted playsinline crossorigin="anonymous" preload="auto" class="max-w-full max-h-full object-contain rounded-xl shadow-lg bg-black pointer-events-auto"></video>
            
            <template v-else-if="isPDF(selectedFile.name)">
              <iframe v-if="!isMobile" :src="previewUrl" class="w-full h-full min-h-[60vh] sm:min-h-[68vh] rounded-xl border border-slate-200 bg-white shadow-inner pointer-events-auto"></iframe>
              <div v-else class="flex flex-col items-center justify-center text-center p-6 bg-slate-50 border border-slate-200/80 rounded-2xl max-w-sm w-full shadow-xs animate-fade-in pointer-events-auto">
                <div class="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center mb-3 border border-amber-100">
                  <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                </div>
                <h4 class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-1">Mobil PDF Deneyimi</h4>
                <p class="text-[11px] text-slate-500 mb-4 leading-relaxed font-medium">Mobil cihazlarda pürüzsüz çoklu sayfa kaydırma ve zoom desteği için dökümanı yerel tam ekran modunda açın.</p>
                <button @click="openPdfInNewTab(selectedFile)" class="w-full py-3.5 bg-theme-primary text-slate-900 font-bold rounded-xl text-xs shadow-xs active:scale-[0.97] transition-all flex items-center justify-center gap-2">
                  <svg class="w-4 h-4 text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                  Dokümanı Yerel Görüntüleyicide Aç
                </button>
              </div>
            </template>
            
            <div class="flex flex-col items-center justify-center text-center p-6 bg-white rounded-2xl border border-slate-200 max-w-xs pointer-events-auto" v-else>
              <h4 class="text-base sm:text-lg font-black text-slate-800 mb-1">{{ t.previewNotSupportedPreview }}</h4>
              <p class="text-xs text-slate-500 mb-4">{{ t.previewNotSupportedDesc }}</p>
              <button @click="downloadItem(selectedFile)" class="flex items-center gap-2 px-5 py-2.5 bg-theme-primary text-slate-900 rounded-xl text-xs font-bold">{{ t.downloadFile }}</button>
            </div>
          </div>

          <button v-if="hasNextFile" @click.stop="nextFile" class="absolute right-2 z-30 w-9 h-9 flex items-center justify-center bg-white/80 hover:bg-white text-slate-800 rounded-full shadow-lg transition-all active:scale-95 border border-slate-200/50 backdrop-blur-sm hidden sm:flex">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showToast" class="fixed bottom-10 left-1/2 transform -translate-x-1/2 bg-emerald-500 text-white px-4 py-2.5 rounded-xl shadow-2xl font-bold text-xs z-50 flex items-center gap-1.5 border border-emerald-400 animate-fade-in transition-all">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
      {{ t.toastCopied }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { currentLang, setLanguage, t } from '../utils/i18n.js'

const router = useRouter()
const API_BASE = window.location.origin

const items = ref([])
const loading = ref(true)
const systemMessage = ref(null)
const selectedFile = ref(null)
const showToast = ref(false)

const userSession = ref(null)

const currentPath = ref("") 
const searchQuery = ref("") 
const viewMode = ref("grid")

const selectedItems = ref([])
const isDownloading = ref(false) 
const downloadingItemId = ref(null) 

const activeDropdownId = ref(null)

const sortBy = ref("name")
const sortOrder = ref("asc")

const touchStartX = ref(0)
const touchEndX = ref(0)
const swipeThreshold = 55 

const previewUrl = ref('')

const isMobile = ref(false)

const checkDevice = () => {
  isMobile.value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 640
}

const handleTouchStart = (e) => {
  touchStartX.value = e.touches[0].clientX
}

const handleTouchEnd = (e) => {
  touchEndX.value = e.changedTouches[0].clientX
  analyzeSwipeGesture()
}

const analyzeSwipeGesture = () => {
  const diffX = touchStartX.value - touchEndX.value
  if (Math.abs(diffX) > swipeThreshold) {
    if (diffX > 0) {
      if (hasNextFile.value) nextFile()
    } else {
      if (hasPrevFile.value) prevFile()
    }
  }
}

let searchTimeout = null;
watch(searchQuery, (newQuery) => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    const trimmed = newQuery.trim()
    if (trimmed) {
      fetchGlobalSearch(trimmed)
    } else {
      fetchFiles(currentPath.value)
    }
  }, 400)
})

const loadPreviewUrl = (item) => {
  if (!item) {
    previewUrl.value = ''
    return
  }
  const baseLink = item.webViewLink ? item.webViewLink.split('?')[0] : ''
  if (isPDF(item.name)) {
    previewUrl.value = `${API_BASE}/api/view/pdf?path=${encodeURIComponent(item.id)}&token=${encodeURIComponent(userSession.value?.token || '')}`
  } else if (isVideo(item.name)) {
    previewUrl.value = baseLink ? `${baseLink}#t=6.0` : ''
  } else {
    previewUrl.value = baseLink
  }
}

watch(selectedFile, (newFile) => {
  loadPreviewUrl(newFile)
})

const previewableFiles = computed(() => {
  return displayItems.value.filter(item => item.mimeType !== 'application/vnd.google-apps.folder')
})

const currentFileIndex = computed(() => {
  if (!selectedFile.value) return -1
  return previewableFiles.value.findIndex(f => f.id === selectedFile.value.id)
})

const hasPrevFile = computed(() => currentFileIndex.value > 0)
const hasNextFile = computed(() => currentFileIndex.value > -1 && currentFileIndex.value < previewableFiles.value.length - 1)

const prevFile = () => {
  if (hasPrevFile.value) {
    selectedFile.value = previewableFiles.value[currentFileIndex.value - 1]
  }
}

const nextFile = () => {
  if (hasNextFile.value) {
    selectedFile.value = previewableFiles.value[currentFileIndex.value + 1]
  }
}

const handleKeyDown = (e) => {
  if (!selectedFile.value) return
  if (e.key === 'ArrowLeft') {
    prevFile()
  } else if (e.key === 'ArrowRight') {
    nextFile()
  } else if (e.key === 'Escape') {
    selectedFile.value = null
  }
}

const handleSort = (column) => {
  if (sortBy.value === column) {
    toggleSortOrder()
  } else {
    sortBy.value = column
    sortOrder.value = 'asc'
  }
}

const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
}

const toggleDropdown = (id) => {
  activeDropdownId.value = activeDropdownId.value === id ? null : id
}

const closeAllDropdowns = () => {
  activeDropdownId.value = null
}

const goToParentFolder = () => {
  if (!currentPath.value) return
  if (['customer', 'müşteri'].includes(userSession.value?.role)) {
    const allowed = userSession.value?.allowedFolders || []
    // 🌟 SÖZDİZİMİ DÜZELTİLDİ: of yerine tek kelime isRootOfAllowed atandı
    const isRootOfAllowed = allowed.some(f => f.id === currentPath.value)
    if (isRootOfAllowed) {
      fetchFiles('') 
      return
    }
  }
  const parts = currentPath.value.split('/')
  parts.pop() 
  const parentPath = parts.join('/')
  fetchFiles(parentPath)
}

const breadcrumbs = computed(() => {
  if (searchQuery.value.trim()) {
    return [{ name: `${t.value.searchResultFor} "${searchQuery.value}"`, path: currentPath.value, isSearch: true }]
  }

  const isCustomer = ['customer', 'müşteri'].includes(userSession.value?.role)
  if (isCustomer) {
    const allowed = userSession.value?.allowedFolders || []
    const matched = allowed.find(f => currentPath.value === f.id || currentPath.value.startsWith(f.id + '/'))
    
    if (matched) {
      const list = []
      list.push({ name: matched.name, path: matched.id })
      
      if (currentPath.value.length > matched.id.length) {
        const subPath = currentPath.value.substring(matched.id.length).replace(/^\/+/, '')
        const parts = subPath.split('/')
        let currentAccumulatedPath = matched.id
        for (const part of parts) {
          if (part) {
            currentAccumulatedPath += '/' + part
            list.push({ name: part, path: currentAccumulatedPath })
          }
        }
      }
      return list
    }
  }

  const parts = currentPath.value.split('/')
  const list = []
  let currentAccumulatedPath = ""
  for (const part of parts) {
    if (part) {
      currentAccumulatedPath = currentAccumulatedPath ? `${currentAccumulatedPath}/${part}` : part
      list.push({ name: part, path: currentAccumulatedPath })
    }
  }
  return list
})

const downloadableItems = computed(() => items.value.filter(i => i.mimeType !== 'application/vnd.google-apps.folder'))
const isAllSelected = computed(() => downloadableItems.value.length > 0 && selectedItems.value.length === downloadableItems.value.length)

const handleLogout = () => {
  localStorage.removeItem('bonna_user_session')
  router.push('/login')
}

const formatSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const shareItem = (item) => {
  if (!item || !item.webViewLink) return
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(item.webViewLink)
      .then(() => {
        showToast.value = true
        setTimeout(() => { showToast.value = false }, 3000)
      })
      .catch(() => fallbackCopyTextToClipboard(item.webViewLink))
  } else {
    fallbackCopyTextToClipboard(item.webViewLink)
  }
}

const fallbackCopyTextToClipboard = (text) => {
  const textArea = document.createElement("textarea")
  // 🌟 SÖZDİZİMİ DÜZELTİLDİ: Tanımlı değişken ismine sadık kalınarak textArea çağrıldı
  textArea.value = text
  textArea.style.position = "fixed"
  textArea.style.left = "-9999px"
  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()
  try {
    if (document.execCommand('copy')) {
      showToast.value = true
      setTimeout(() => { showToast.value = false }, 3000)
    }
  } catch (err) {
    console.error("Kopyalama başarısız:", err)
  }
  document.body.removeChild(textArea)
}

const isSelected = (item) => selectedItems.value.some(i => i.id === item.id)
const toggleSelection = (item) => {
  if (item.mimeType === 'application/vnd.google-apps.folder') return
  const index = selectedItems.value.findIndex(i => i.id === item.id)
  if (index > -1) selectedItems.value.splice(index, 1)
  else selectedItems.value.push(item)
}

const toggleSelectAll = () => { isAllSelected.value ? clearSelection() : selectedItems.value = [...downloadableItems.value] }
const clearSelection = () => { selectedItems.value = [] }

const downloadSingleFile = async (fileItem) => {
  try {
    const response = await axios.get(`${API_BASE}/download/file?path=${encodeURIComponent(fileItem.id)}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', fileItem.name)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error("Download error:", error)
  }
}

const downloadZip = async (targets) => {
  isDownloading.value = true
  try {
    const response = await axios.post(`${API_BASE}/download/zip`, { 
      paths: targets.map(i => i.id)
    }, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'BonnaCloud_Export.zip')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error("Zip creation error:", error)
  } finally { 
    isDownloading.value = false 
  }
}

const downloadItem = async (item) => {
  downloadingItemId.value = item.id
  if (item.mimeType !== 'application/vnd.google-apps.folder') {
    await downloadSingleFile(item)
  }
  downloadingItemId.value = null
}

const downloadSelected = async () => {
  if (selectedItems.value.length === 0) return
  if (selectedItems.value.length === 1) {
    await downloadSingleFile(selectedItems.value[0])
    clearSelection()
    return
  }
  await downloadZip(selectedItems.value)
  clearSelection()
}

const openPdfInNewTab = (item) => {
  if (!item) return
  const url = `${API_BASE}/api/view/pdf?path=${encodeURIComponent(item.id)}&token=${encodeURIComponent(userSession.value?.token || '')}`
  window.open(url, '_blank')
}

const isVideo = (filename) => ['mp4', 'webm', 'ogg', 'mov', 'avi'].includes(filename.split('.').pop().toLowerCase())
const isImage = (filename) => ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'tiff', 'tif'].includes(filename.split('.').pop().toLowerCase())
const isPDF = (filename) => filename.split('.').pop().toLowerCase() === 'pdf'

const isWord = (filename) => ['docx', 'doc'].includes(filename.split('.').pop().toLowerCase())
const isExcel = (filename) => ['xlsx', 'xls', 'csv'].includes(filename.split('.').pop().toLowerCase())
const isPPTX = (filename) => ['pptx', 'ppt'].includes(filename.split('.').pop().toLowerCase())

const getExtension = (filename) => filename.split('.').pop().toUpperCase()

const getPreviewUrl = (item, mode) => {
  if (!item.webViewLink) return ''
  const baseLink = item.webViewLink.split('?')[0]
  if (isVideo(item.name)) {
    return mode === 'preview' ? baseLink : `${baseLink}#t=6.0`
  }
  if (isPDF(item.name) || isWord(item.name) || isExcel(item.name) || isPPTX(item.name)) {
    return baseLink
  }
  if (mode === 'list') return `${baseLink}?width=40&quality=40`
  if (mode === 'grid') return `${baseLink}?width=200&quality=65`
  return baseLink
}

const goToRoot = () => { 
  searchQuery.value = "" 
  fetchFiles('') 
}

const fetchFiles = async (path = "") => {
  loading.value = true
  systemMessage.value = null
  clearSelection() 
  closeAllDropdowns() 

  try {
    const response = await axios.get(`${API_BASE}/files?path=${encodeURIComponent(path)}`)
    if (response.data.error) {
      systemMessage.value = response.data.error
      items.value = []
    } else {
      items.value = response.data.files || [] 
      currentPath.value = path
    }
  } catch (error) {
    systemMessage.value = "Cannot access the cloud server (backend). Please check your Docker containers."
  } finally {
    loading.value = false
  }
}

const handleItemClick = (item) => {
  if (selectedItems.value.length > 0) {
    if (item.mimeType !== 'application/vnd.google-apps.folder') toggleSelection(item)
    return
  }
  if (item.mimeType === 'application/vnd.google-apps.folder') {
    searchQuery.value = "" 
    fetchFiles(item.id) 
  } else {
    if (isMobile.value && isPDF(item.name)) {
      openPdfInNewTab(item)
    } else {
      selectedFile.value = item
    }
  }
}

const displayItems = computed(() => {
  let filteredList = [...items.value]
  return filteredList.sort((a, b) => {
    const isFolderA = a.mimeType === 'application/vnd.google-apps.folder' ? 1 : 0
    const isFolderB = b.mimeType === 'application/vnd.google-apps.folder' ? 1 : 0
    if (isFolderA !== isFolderB) return isFolderB - isFolderA

    if (sortBy.value === 'name') {
      return sortOrder.value === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name)
    } 
    else if (sortBy.value === 'size') {
      if (isFolderA) return a.name.localeCompare(b.name)
      return sortOrder.value === 'asc' ? a.size - b.size : b.size - a.size
    }
    return 0
  })
})

onMounted(() => {
  checkDevice()
  window.addEventListener('resize', checkDevice)
  
  userSession.value = JSON.parse(localStorage.getItem('bonna_user_session') || 'null')
  if (userSession.value && userSession.value.token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${userSession.value.token}`
  }
  fetchFiles()
  window.addEventListener('click', closeAllDropdowns)
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkDevice)
  window.removeEventListener('click', closeAllDropdowns)
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>