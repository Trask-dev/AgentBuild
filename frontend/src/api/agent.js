import api from './index'

export const getAgents   = ()          => api.get('/agent')
export const getAgent    = (id)        => api.get(`/agent/${id}`)
export const createAgent = (data)      => api.post('/agent', data)
export const updateAgent = (id, data)  => api.put(`/agent/${id}`, data)
export const deleteAgent = (id)        => api.delete(`/agent/${id}`)
