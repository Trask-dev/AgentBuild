<template>
  <div class="page">
    <div class="page-head">
      <h2>知识库</h2>
      <el-button type="primary" @click="openCreate">新建知识库</el-button>
    </div>

    <div v-loading="loading" class="card-grid">
      <el-empty v-if="!loading && list.length===0" description="暂无知识库" />
      <div v-for="r in list" :key="r.id" class="card">
        <div class="card-top">
          <div class="card-icon"><el-icon :size="22"><FolderOpened /></el-icon></div>
          <div>
            <div class="card-name">{{ r.name }}</div>
            <div class="card-desc">{{ r.description || '暂无描述' }}</div>
          </div>
        </div>
        <div class="card-meta">创建于 {{ r.created_time?.slice(0,10) }}</div>
        <div class="card-acts">
          <el-upload
            :action="`/rag/${r.id}/upload`"
            :show-file-list="false"
            accept=".txt,.pdf"
            @success="onUploadOk"
            @error="onUploadFail"
          >
            <el-button size="small" text>上传文件</el-button>
          </el-upload>
          <el-button size="small" text @click="openEdit(r)">编辑</el-button>
          <el-button size="small" text type="danger" @click="doDelete(r)">删除</el-button>
        </div>
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingId ? '编辑知识库' : '新建知识库'"
      width="480px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="知识库名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="描述知识库的内容" />
        </el-form-item>
      </el-form>

      <!-- 编辑模式下显示上传区 -->
      <div v-if="editingId" style="margin-top:8px">
        <el-divider />
        <p style="font-size:13px;color:var(--text-tertiary);margin-bottom:12px;">上传文件（支持 .txt / .pdf）</p>
        <el-upload
          :action="`/rag/${editingId}/upload`"
          :show-file-list="true"
          accept=".txt,.pdf"
          drag
          @success="onUploadOk"
          @error="onUploadFail"
        >
          <el-icon :size="32"><UploadFilled /></el-icon>
          <div style="font-size:13px;color:var(--text-tertiary);margin-top:8px;">拖拽或点击上传</div>
        </el-upload>
      </div>

      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useAppStore } from '../stores/app'
import { getRags, createRag, updateRag, deleteRag } from '../api/rag'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useAppStore()
const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({ name: '', description: '' })
const rules = { name: [{ required: true, message: '必填', trigger: 'blur' }] }

async function load() {
  loading.value = true
  try { list.value = (await getRags()).data }
  catch { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

onMounted(async () => {
  store.setMenuActive('knowledge')
  await load()
})

function resetForm() { form.name = ''; form.description = '' }

function openCreate() { editingId.value = null; resetForm(); dialogVisible.value = true }

async function openEdit(r) {
  editingId.value = r.id
  form.name = r.name; form.description = r.description || ''
  dialogVisible.value = true
}

async function submit() {
  const ok = await formRef.value.validate().catch(() => false)
  if (!ok) return
  submitting.value = true
  try {
    if (editingId.value) {
      await updateRag(editingId.value, { ...form, avatar: null })
      ElMessage.success('已更新')
    } else {
      await createRag({ ...form, avatar: null })
      ElMessage.success('已创建')
    }
    dialogVisible.value = false
    await load()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally { submitting.value = false }
}

async function doDelete(r) {
  try {
    await ElMessageBox.confirm(`确定删除「${r.name}」？`, '确认', { type: 'warning' })
    await deleteRag(r.id)
    ElMessage.success('已删除')
    await load()
  } catch {}
}

function onUploadOk()  { ElMessage.success('上传导入成功'); load() }
function onUploadFail() { ElMessage.error('上传失败') }
</script>

<style scoped>
.page { height:100%; overflow-y:auto; padding:28px 32px; }
.page-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; }
.page-head h2 { font-size:22px; font-weight:600; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(320px,1fr)); gap:16px; }
.card {
  background:var(--bg-primary); border:1px solid var(--border);
  border-radius:var(--radius-lg); padding:20px;
  display:flex; flex-direction:column; gap:12px;
}
.card-top { display:flex; gap:14px; align-items:flex-start; }
.card-icon {
  width:44px; height:44px; border-radius:12px;
  background:var(--accent-light); color:var(--accent);
  display:flex; align-items:center; justify-content:center;
  flex-shrink:0;
}
.card-name { font-size:16px; font-weight:600; }
.card-desc { font-size:13px; color:var(--text-tertiary); margin-top:2px; }
.card-meta { font-size:12px; color:var(--text-tertiary); }
.card-acts { display:flex; gap:4px; border-top:1px solid var(--border); padding-top:12px; }
</style>
