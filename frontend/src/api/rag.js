import api from './index'

export const getRags     = ()            => api.get('/rag')
export const getRag      = (id)          => api.get(`/rag/${id}`)
export const createRag   = (data)        => api.post('/rag', data)
export const updateRag   = (id, data)    => api.put(`/rag/${id}`, data)
export const deleteRag   = (id)          => api.delete(`/rag/${id}`)
export const uploadFile  = (ragId, file) => {
  const fd = new FormData()
  fd.append('file', file)
  return api.post(`/rag/${ragId}/upload`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
