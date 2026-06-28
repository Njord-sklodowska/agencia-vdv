/**
 * Formatea un DNI/CUIT al formato visual según tipo de persona
 * - Persona Física: muestra DNI de 8 dígitos sin guiones (ej: 23123456)
 * - Persona Jurídica: muestra CUIT con guiones (ej: 30-23213354-5)
 * @param {string} value - Valor limpio (sin guiones)
 * @param {string} tipoPersona - 'fisica' o 'juridica'
 */
export const formatDniCuit = (value, tipoPersona) => {
  if (!value) return '---';

  // Quitar todo lo que no sea número
  const cleaned = value.toString().replace(/[^\d]/g, '');

  if (tipoPersona === 'fisica') {
    // DNI: mostrar 8 dígitos sin formato
    return cleaned;
  } else {
    // CUIT: formato XX-XXXXXXXX-X (11 dígitos)
    if (cleaned.length === 11) {
      return `${cleaned.slice(0, 2)}-${cleaned.slice(2, 10)}-${cleaned.slice(10)}`;
    }
    return cleaned;
  }
};

/**
 * Formatea un CUIL al formato XX-XXXXXXXX-X
 * @param {string} value - Valor limpio (11 dígitos sin guiones)
 */
export const formatCuil = (value) => {
  if (!value) return '---';
  
  const cleaned = value.toString().replace(/[^\d]/g, '');
  
  if (cleaned.length === 11) {
    return `${cleaned.slice(0, 2)}-${cleaned.slice(2, 10)}-${cleaned.slice(10)}`;
  }
  
  return cleaned;
};

/**
 * Formatea un número de teléfono al formato (XXX) XXX-XXXX
 */
export const formatTelefono = (value) => {
  if (!value) return '---';
  const cleaned = value.toString().replace(/[^\d]/g, '');
  if (cleaned.length >= 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6, 10)}`;
  }
  if (cleaned.length >= 6) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3)}`;
  }
  return value;
};
