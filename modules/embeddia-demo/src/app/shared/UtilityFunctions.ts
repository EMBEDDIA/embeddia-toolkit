export class UtilityFunctions {
  static readonly COLORS = {
    ORG: '#b71c1c',
    PER: '#880e4f',
    GPE: '#4a148c',
    LOC: '#311b92',
    ADDR: '#0d47a1',
    COMPANY: '#006064',
    PHO: '#1b5e20',
    EMAIL: '#3e2723',
    KEYWORD: '#263238'
  };

  static typeGuard<T>(o, className: { new(...args: any[]): T }): o is T {
    return o instanceof className;
  }

  static propertiesToArray<T, K extends keyof T>(o: T, propertyNames: K[]): T[K][] {
    return propertyNames.map(n => o[n]);
  }

  /*
  * check if each array element exists in both arrays for each element
  * */
  static arrayValuesEqual(arr1: string[], arr2: string[]): boolean {
    if (arr1.length === arr2.length) {
      return arr1.every(x => arr2.includes(x));
    } else {
      return false;
    }
  }

  static sortByStringProperty<T>(object: T[], propertyAccessor: (x: T) => string): T[] {
    return object.sort((a, b) => {
      const propertyA = propertyAccessor(a).toUpperCase();
      const propertyB = propertyAccessor(b).toUpperCase();
      if (propertyA < propertyB) {
        return -1;
      }
      if (propertyA > propertyB) {
        return 1;
      }
      // names must be equal
      return 0;
    });
  }

  static getDistinctByProperty<T>(objectArray: T[], propertyAccessor: (x: T) => any): T[] {
    const distinct: T[] = [];
    const unique: boolean[] = [];
    for (const el of objectArray) {
      if (!unique[propertyAccessor(el)]) {
        distinct.push(el);
        unique[propertyAccessor(el)] = true;
      }
    }
    return distinct;
  }
}
