{{- define "app.image" -}}
{{- $registryName := .Values.deployment.image.registry -}}
{{- $repositoryName := .Values.deployment.image.repository | default .Chart.Name -}}
{{- $tag := .Values.deployment.image.tag }}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- end -}}

