import api from './index'

export const getSessions    = (agentId) => api.get('/session', { params: agentId ? { agent_id: agentId } : {} })
export const getSession     = (id)      => api.get(`/session/${id}`)
export const createSession  = (data)    => api.post('/session', data)
export const updateSession  = (id, data)=> api.put(`/session/${id}`, data)
export const deleteSession  = (id)      => api.delete(`/session/${id}`)
