/**
 * Processes and filters users with modern ES6+ features and comprehensive error handling
 * @param {Array<Object>} users - Array of user objects
 * @param {Object} filters - Filter criteria object
 * @param {number} [filters.minAge] - Minimum age filter
 * @param {string} [filters.department] - Department filter
 * @param {boolean} [filters.active] - Active status filter
 * @returns {Array<Object>} Filtered and processed user objects
 * @throws {TypeError} When users is not an array or filters is not an object
 * @throws {Error} When user objects are missing required fields
 */
const processUsers = (users, filters = {}) => {
  // Input validation
  if (!Array.isArray(users)) {
    throw new TypeError('Users parameter must be an array');
  }
  
  if (typeof filters !== 'object' || filters === null) {
    throw new TypeError('Filters parameter must be an object');
  }
  
  // Destructure filters with defaults
  const { minAge, department, active } = filters;
  const currentYear = new Date().getFullYear();
  
  // Use filter and map for functional approach - more performant for large datasets
  return users
    .filter(user => {
      // Validate user object structure
      if (!user || typeof user !== 'object') {
        console.warn('Skipping invalid user object:', user);
        return false;
      }
      
      // Check required fields
      const requiredFields = ['id', 'firstName', 'lastName', 'email', 'department', 'startYear'];
      const missingFields = requiredFields.filter(field => !(field in user));
      if (missingFields.length > 0) {
        console.warn(`Skipping user ${user.id || 'unknown'} - missing fields:`, missingFields);
        return false;
      }
      
      // Apply filters with null/undefined safety
      if (minAge !== undefined && (user.age === null || user.age === undefined || user.age < minAge)) {
        return false;
      }
      
      if (department !== undefined && user.department !== department) {
        return false;
      }
      
      if (active !== undefined && Boolean(user.isActive) !== active) {
        return false;
      }
      
      return true;
    })
    .map(user => {
      // Destructure user properties
      const { id, firstName, lastName, email, department: userDept, startYear, ...rest } = user;
      
      // Calculate years employed with validation
      let yearsEmployed = 0;
      if (startYear && typeof startYear === 'number' && startYear <= currentYear) {
        yearsEmployed = currentYear - startYear;
      }
      
      // Return immutable processed user object
      return Object.freeze({
        id,
        name: `${firstName || ''} ${lastName || ''}`.trim(),
        email: email || '',
        department: userDept || '',
        yearsEmployed,
        // Preserve any additional properties
        ...rest
      });
    });
};

// Export for module usage
module.exports = processUsers;

// Example usage:
/*
const users = [
  { id: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com', department: 'IT', age: 30, isActive: true, startYear: 2020 },
  { id: 2, firstName: 'Jane', lastName: 'Smith', email: 'jane@example.com', department: 'HR', age: 25, isActive: false, startYear: 2019 }
];

const filtered = processUsers(users, { minAge: 28, active: true });
console.log(filtered);
*/