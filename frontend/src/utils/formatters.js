/**
 * Formatea un DNI/CUIT al formato visual XX-XXXXXXXX-X
 * - DNI: XX-XXXXXXX-X (ej: 20-797957-4)
 * - CUIT: XX-XXXXXXXX-X (ej: 20-12345678-9)
 */
export const formatDniCuit = (value) => {
  if (!value) return '---';

  // Quitar todo lo que no sea número
  const cleaned = value.toString().replace(/[^\d]/g, '');

  if (cleaned.length >= 10) {
    // CUIT: XX-XXXXXXXX-X (11 dígitos)
    return `${cleaned.slice(0, 2)}-${cleaned.slice(2, 10)}-${cleaned.slice(10, 11)}`;
  }

  if (cleaned.length >= 8) {
    // DNI: XX-XXXXXXX-X (8-9 dígitos)
    // Ej: 20797957-4 → 20-797957-4
    // Ej: 207979574 → 20-7979574
    const prefix = cleaned.slice(0, 2);
    const suffix = cleaned.slice(-1);
    const middle = cleaned.slice(2, -1);
    return `${prefix}-${middle}-${suffix}`;
  }

  if (cleaned.length >= 6) {
    // DNI corto: XX-XXXXXX
    return `${cleaned.slice(0, 2)}-${cleaned.slice(2)}`;
  }

  // Si no coincide con ningún formato conocido, devolver tal cual
  return value;
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
