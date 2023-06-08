/**
 * Checks if eventDefinition of the given element matches with semantic type.
 *
 * @param event
 * @param eventDefinitionType
 *
 * @return
 */
export function isTypedEvent(event: any, eventDefinitionType: string): boolean;
/**
 * Check if element is a throw event.
 *
 * @param event
 *
 * @return
 */
export function isThrowEvent(event: any): boolean;
/**
 * Check if element is a throw event.
 *
 * @param element
 *
 * @return
 */
export function isCollection(element: any): boolean;
/**
 * @param element
 * @param defaultColor
 *
 * @return
 */
export function getFillColor(element: any, defaultColor?: string): string;
/**
 * @param element
 * @param defaultColor
 *
 * @return
 */
export function getStrokeColor(element: any, defaultColor?: string): string;
/**
 * @param element
 * @param defaultColor
 * @param defaultStrokeColor
 *
 * @return
 */
export function getLabelColor(element: any, defaultColor?: string, defaultStrokeColor?: string): string;
/**
 * @param shape
 *
 * @return path
 */
export function getCirclePath(shape: any): string;
/**
 * @param shape
 * @param borderRadius
 *
 * @return path
 */
export function getRoundRectPath(shape: any, borderRadius?: number): string;
/**
 * @param shape
 *
 * @return path
 */
export function getDiamondPath(shape: any): string;
/**
 * @param shape
 *
 * @return path
 */
export function getRectPath(shape: any): string;
export const black: string;
export type ModdleElement = any;
export type Element = any;
export type ShapeLike = any;
export { getDi, getBusinessObject as getSemantic } from "../util/ModelUtil";
