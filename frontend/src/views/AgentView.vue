<template>
  <div class="page">
    <div class="page-head">
      <h2>智能体</h2>
      <el-button type="primary" @click="openCreate">新建智能体</el-button>
    </div>

    <div v-loading="loading" class="card-grid">
      <el-empty v-if="!loading && list.length===0" description="暂无智能体" />
      <div v-for="a in list" :key="a.id" class="card" @click="openEdit(a)">
        <div class="card-top">
          <span class="card-name">{{ a.name }}</span>
          <el-tag size="small" round>{{ a.model_name }}</el-tag>
        </div>
        <div class="card-desc">{{ a.description || '暂无描述' }}</div>
        <div class="card-prompt" v-if="a.system_prompt">{{ a.system_prompt.slice(0,100) }}{{ a.system_prompt.length>100?'...':'' }}</div>
        <div class="card-acts" @click.stop>
          <el-button size="small" text @click="startChat(a)">对话</el-button>
          <el-button size="small" text @click="openEdit(a)">编辑</el-button>
          <el-button size="small" text type="danger" @click="doDelete(a)">删除</el-button>
        </div>
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingId ? '编辑智能体' : '新建智能体'"
      width="560px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="智能体名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" placeholder="简要描述" />
        </el-form-item>
        <el-form-item label="系统提示词" prop="system_prompt">
          <el-input v-model="form.system_prompt" type="textarea" :rows="5" placeholder="设定智能体的角色与行为..." />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="模型名称" prop="model_name">
              <el-input v-model="form.model_name" placeholder="qwen-max" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="API Key" prop="api_key">
              <el-input v-model="form.api_key" type="password" show-password placeholder="sk-..." />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="API Base URL" prop="base_url">
          <el-input v-model="form.base_url" placeholder="https://dashscope.aliyuncs.com/compatible-mode/v1" />
        </el-form-item>
        <el-form-item label="绑定知识库">
          <el-select v-model="form.kb_id" placeholder="可选" clearable style="width:100%">
            <el-option v-for="r in ragOptions" :key="r.id" :label="r.name" :value="r.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { getAgents, getAgent, createAgent, updateAgent, deleteAgent } from '../api/agent'
import { getRags } from '../api/rag'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const store = useAppStore()

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const ragOptions = ref([])
const formRef = ref(null)

const form = reactive({
  name: '', description: '', system_prompt: '',
  model_name: '', api_key: '', base_url: '', kb_id: null
})

const rules = {
  name:          [{ required: true, message: '必填', trigger: 'blur' }],
  system_prompt: [{ required: true, message: '必填', trigger: 'blur' }],
  model_name:    [{ required: true, message: '必填', trigger: 'blur' }],
  base_url:      [{ required: true, message: '必填', trigger: 'blur' }]
}

async function load() {
  loading.value = true
  try { const r = await getAgents(); list.value = r.data; store.setAgents(r.data) }
  catch { ElMessage.error('加载失败') }
  finally { loading.value = false }
}

onMounted(async () => {
  store.setMenuActive('agents')
  await load()
  try { ragOptions.value = (await getRags()).data } catch {}
})

function resetForm() {
  form.name = ''; form.description = ''; form.system_prompt = ''
  form.model_name = ''; form.api_key = ''; form.base_url = ''; form.kb_id = null
}

function openCreate() { editingId.value = null; resetForm(); dialogVisible.value = true }

async function openEdit(a) {
  editingId.value = a.id
  try {
    const r = await getAgent(a.id)
    const d = r.data
    form.name = d.name; form.description = d.description || ''
    form.system_prompt = d.system_prompt; form.model_name = d.model_name
    form.api_key = d.api_key; form.base_url = d.base_url; form.kb_id = d.kb_id
    dialogVisible.value = true
  } catch (e) {
    console.error('获取智能体详情失败', e)
    ElMessage.error('获取详情失败：' + (e.response?.data?.detail || e.message || '未知错误'))
  }
}

async function submit() {
  // 编辑模式 api_key 非必填，新建模式必填
  if (!editingId.value && !form.api_key.trim()) {
    ElMessage.warning('请输入 API Key')
    return
  }
  const ok = await formRef.value.validate().catch(() => false)
  if (!ok) return
  submitting.value = true
  try {
    const data = { ...form, tools: [] }
    // 编辑时 api_key 含 **** 说明是脱敏值未修改，后端应保留原值
    if (editingId.value) {
      await updateAgent(editingId.value, data)
      ElMessage.success('已更新')
    } else {
      await createAgent(data)
      ElMessage.success('已创建')
    }
    dialogVisible.value = false
    await load()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally { submitting.value = false }
}

async function doDelete(a) {
  try {
    await ElMessageBox.confirm(`确定删除「${a.name}」？`, '确认', { type: 'warning' })
    await deleteAgent(a.id)
    ElMessage.success('已删除')
    await load()
  } catch {}
}

function startChat(a) {
  store.setCurrentAgent(a)
  store.setCurrentSession(null)
  store.setMenuActive('chat')
  router.push('/chat')
}
</script>

<style scoped>
.page { height:100%; overflow-y:auto; padding:28px 32px; }
.page-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; }
.page-head h2 { font-size:22px; font-weight:600; }
.card-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(320px,1fr)); gap:16px; }
.card {
  background:var(--bg-primary); border:1px solid var(--border);
  border-radius:var(--radius-lg); padding:20px; cursor:pointer;
  transition:box-shadow .2s; display:flex; flex-direction:column; gap:10px;
}
.card:hover { box-shadow:var(--shadow-md); }
.card-top { display:flex; justify-content:space-between; align-items:center; }
.card-name { font-size:16px; font-weight:600; }
.card-desc { font-size:13px; color:var(--text-tertiary); }
.card-prompt { font-size:12px; color:var(--text-secondary); line-height:1.5; background:var(--bg-secondary); padding:10px; border-radius:var(--radius-sm); }
.card-acts { display:flex; gap:4px; margin-top:4px; border-top:1px solid var(--border); padding-top:12px; }
</style>
