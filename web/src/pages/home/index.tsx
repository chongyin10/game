import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { User, Lock, Eye, EyeOff, Sparkles, Sword, Star, Flame, Wind } from 'lucide-react'
import { Input, Button, message } from '@zjpcy/simple-design'
import { login, register } from '@/api'
import type { ApiResponse, LoginData, RegisterData } from '@/types'
import './index.css'

// MD5 加密函数
function md5(str: string): string {
  function rotateLeft(lValue: number, iShiftBits: number): number {
    return (lValue << iShiftBits) | (lValue >>> (32 - iShiftBits))
  }

  function addUnsigned(lX: number, lY: number): number {
    const lX8 = lX & 0x80000000
    const lY8 = lY & 0x80000000
    const lX4 = lX & 0x40000000
    const lY4 = lY & 0x40000000
    const lResult = (lX & 0x3FFFFFFF) + (lY & 0x3FFFFFFF)
    if (lX4 & lY4) return lResult ^ 0x80000000 ^ lX8 ^ lY8
    if (lX4 | lY4) {
      if (lResult & 0x40000000) return lResult ^ 0xC0000000 ^ lX8 ^ lY8
      return lResult ^ 0x40000000 ^ lX8 ^ lY8
    }
    return lResult ^ lX8 ^ lY8
  }

  function f(x: number, y: number, z: number): number { return (x & y) | ((~x) & z) }
  function g(x: number, y: number, z: number): number { return (x & z) | (y & (~z)) }
  function h(x: number, y: number, z: number): number { return x ^ y ^ z }
  function i(x: number, y: number, z: number): number { return y ^ (x | (~z)) }

  function ff(a: number, b: number, c: number, d: number, x: number, s: number, ac: number): number {
    return addUnsigned(rotateLeft(addUnsigned(addUnsigned(a, f(b, c, d)), addUnsigned(x, ac)), s), b)
  }
  function gg(a: number, b: number, c: number, d: number, x: number, s: number, ac: number): number {
    return addUnsigned(rotateLeft(addUnsigned(addUnsigned(a, g(b, c, d)), addUnsigned(x, ac)), s), b)
  }
  function hh(a: number, b: number, c: number, d: number, x: number, s: number, ac: number): number {
    return addUnsigned(rotateLeft(addUnsigned(addUnsigned(a, h(b, c, d)), addUnsigned(x, ac)), s), b)
  }
  function ii(a: number, b: number, c: number, d: number, x: number, s: number, ac: number): number {
    return addUnsigned(rotateLeft(addUnsigned(addUnsigned(a, i(b, c, d)), addUnsigned(x, ac)), s), b)
  }

  let k: number
  let AA: number = 1732584193
  let BB: number = -271733879
  let CC: number = -1732584194
  let DD: number = 271733878
  let a: number
  let b: number
  let c: number
  let d: number
  const S11 = 7, S12 = 12, S13 = 17, S14 = 22
  const S21 = 5, S22 = 9, S23 = 14, S24 = 20
  const S31 = 4, S32 = 11, S33 = 16, S34 = 23
  const S41 = 6, S42 = 10, S43 = 15, S44 = 21

  str = unescape(encodeURIComponent(str))
  const strLen = str.length
  const wordArray: number[] = []
  
  for (let i = 0; i < strLen - 1; i += 4) {
    wordArray.push(
      str.charCodeAt(i) |
      (str.charCodeAt(i + 1) << 8) |
      (str.charCodeAt(i + 2) << 16) |
      (str.charCodeAt(i + 3) << 24)
    )
  }

  switch (strLen % 4) {
    case 0:
      k = 0x080000000
      break
    case 1:
      k = str.charCodeAt(strLen - 1) | 0x0800000
      break
    case 2:
      k = str.charCodeAt(strLen - 2) | (str.charCodeAt(strLen - 1) << 8) | 0x08000
      break
    default:
      k = str.charCodeAt(strLen - 3) | (str.charCodeAt(strLen - 2) << 8) | (str.charCodeAt(strLen - 1) << 16) | 0x80
  }
  wordArray.push(k)

  while ((wordArray.length % 16) !== 14) wordArray.push(0)
  wordArray.push(strLen >>> 29)
  wordArray.push((strLen << 3) & 0x0ffffffff)

  for (let i = 0; i < wordArray.length; i += 16) {
    a = AA = 1732584193
    b = BB = -271733879
    c = CC = -1732584194
    d = DD = 271733878

    a = ff(a, b, c, d, wordArray[i + 0], S11, -680876936)
    d = ff(d, a, b, c, wordArray[i + 1], S12, -389564586)
    c = ff(c, d, a, b, wordArray[i + 2], S13, 606105819)
    b = ff(b, c, d, a, wordArray[i + 3], S14, -1044525330)
    a = ff(a, b, c, d, wordArray[i + 4], S11, -176418897)
    d = ff(d, a, b, c, wordArray[i + 5], S12, 1200080426)
    c = ff(c, d, a, b, wordArray[i + 6], S13, -1473231341)
    b = ff(b, c, d, a, wordArray[i + 7], S14, -45705983)
    a = ff(a, b, c, d, wordArray[i + 8], S11, 1770035416)
    d = ff(d, a, b, c, wordArray[i + 9], S12, -1958414417)
    c = ff(c, d, a, b, wordArray[i + 10], S13, -42063)
    b = ff(b, c, d, a, wordArray[i + 11], S14, -1990404162)
    a = ff(a, b, c, d, wordArray[i + 12], S11, 1804603682)
    d = ff(d, a, b, c, wordArray[i + 13], S12, -40341101)
    c = ff(c, d, a, b, wordArray[i + 14], S13, -1502002290)
    b = ff(b, c, d, a, wordArray[i + 15], S14, 1236535329)

    a = gg(a, b, c, d, wordArray[i + 1], S21, -165796510)
    d = gg(d, a, b, c, wordArray[i + 6], S22, -1069501632)
    c = gg(c, d, a, b, wordArray[i + 11], S23, 643717713)
    b = gg(b, c, d, a, wordArray[i + 0], S24, -373897302)
    a = gg(a, b, c, d, wordArray[i + 5], S21, -701558691)
    d = gg(d, a, b, c, wordArray[i + 10], S22, 38016083)
    c = gg(c, d, a, b, wordArray[i + 15], S23, -660478335)
    b = gg(b, c, d, a, wordArray[i + 4], S24, -405537848)
    a = gg(a, b, c, d, wordArray[i + 9], S21, 568446438)
    d = gg(d, a, b, c, wordArray[i + 14], S22, -1019803690)
    c = gg(c, d, a, b, wordArray[i + 3], S23, -187363961)
    b = gg(b, c, d, a, wordArray[i + 8], S24, 1163531501)
    a = gg(a, b, c, d, wordArray[i + 13], S21, -1444681467)
    d = gg(d, a, b, c, wordArray[i + 2], S22, -51403784)
    c = gg(c, d, a, b, wordArray[i + 7], S23, 1735328473)
    b = gg(b, c, d, a, wordArray[i + 12], S24, -1926607734)

    a = hh(a, b, c, d, wordArray[i + 5], S31, -378558)
    d = hh(d, a, b, c, wordArray[i + 8], S32, -2022574463)
    c = hh(c, d, a, b, wordArray[i + 11], S33, 1839030562)
    b = hh(b, c, d, a, wordArray[i + 14], S34, -35309556)
    a = hh(a, b, c, d, wordArray[i + 1], S31, -1530992060)
    d = hh(d, a, b, c, wordArray[i + 4], S32, 1272893353)
    c = hh(c, d, a, b, wordArray[i + 7], S33, -155497632)
    b = hh(b, c, d, a, wordArray[i + 10], S34, -1094730640)
    a = hh(a, b, c, d, wordArray[i + 13], S31, 681279174)
    d = hh(d, a, b, c, wordArray[i + 0], S32, -358537222)
    c = hh(c, d, a, b, wordArray[i + 3], S33, -722521979)
    b = hh(b, c, d, a, wordArray[i + 6], S34, 76029189)
    a = hh(a, b, c, d, wordArray[i + 9], S31, -640364487)
    d = hh(d, a, b, c, wordArray[i + 12], S32, -421815835)
    c = hh(c, d, a, b, wordArray[i + 15], S33, 530742520)
    b = hh(b, c, d, a, wordArray[i + 2], S34, -995338651)

    a = ii(a, b, c, d, wordArray[i + 0], S41, -198630844)
    d = ii(d, a, b, c, wordArray[i + 7], S42, 1126891415)
    c = ii(c, d, a, b, wordArray[i + 14], S43, -1416354905)
    b = ii(b, c, d, a, wordArray[i + 5], S44, -57434055)
    a = ii(a, b, c, d, wordArray[i + 12], S41, 1700485571)
    d = ii(d, a, b, c, wordArray[i + 3], S42, -1894986606)
    c = ii(c, d, a, b, wordArray[i + 10], S43, -1051523)
    b = ii(b, c, d, a, wordArray[i + 1], S44, -2054922799)
    a = ii(a, b, c, d, wordArray[i + 8], S41, 1873313359)
    d = ii(d, a, b, c, wordArray[i + 15], S42, -30611744)
    c = ii(c, d, a, b, wordArray[i + 6], S43, -1561988384)
    b = ii(b, c, d, a, wordArray[i + 13], S44, 1309151649)
    a = ii(a, b, c, d, wordArray[i + 4], S41, -145523070)
    d = ii(d, a, b, c, wordArray[i + 11], S42, -1120210379)
    c = ii(c, d, a, b, wordArray[i + 2], S43, 718787259)
    b = ii(b, c, d, a, wordArray[i + 9], S44, -343485551)

    AA = addUnsigned(AA, a)
    BB = addUnsigned(BB, b)
    CC = addUnsigned(CC, c)
    DD = addUnsigned(DD, d)
  }

  const result = [AA, BB, CC, DD].map(n => {
    let hex = ''
    for (let j = 0; j <= 3; j++) {
      hex += String.fromCharCode((n >>> (j * 8)) & 255)
    }
    return hex
  }).join('')

  let output = ''
  for (let i = 0; i < result.length; i++) {
    const c = result.charCodeAt(i)
    output += (c < 16 ? '0' : '') + c.toString(16)
  }
  return output
}

type AuthMode = 'login' | 'register'

interface FormData {
  username: string
  password: string
  confirmPassword: string
}

export default function HomePage() {
  const [authMode, setAuthMode] = useState<AuthMode>('login')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [formData, setFormData] = useState<FormData>({
    username: '',
    password: '',
    confirmPassword: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleInputChange = (field: keyof FormData) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }))
  }

  // 验证用户名
  const validateUsername = (username: string): { valid: boolean; message: string } => {
    if (!username || username.length < 3) {
      return { valid: false, message: '用户名长度至少为3个字符' }
    }
    if (username.length > 50) {
      return { valid: false, message: '用户名长度不能超过50个字符' }
    }
    if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(username)) {
      return { valid: false, message: '用户名只能包含字母、数字、下划线或中文' }
    }
    return { valid: true, message: '' }
  }

  // 验证密码
  const validatePassword = (password: string): { valid: boolean; message: string } => {
    if (!password) {
      return { valid: false, message: '密码不能为空' }
    }
    if (password.length < 6) {
      return { valid: false, message: '密码长度至少为6个字符' }
    }
    if (password.length > 128) {
      return { valid: false, message: '密码长度不能超过128个字符' }
    }
    return { valid: true, message: '' }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // 前端校验
    if (authMode === 'login') {
      // 登录校验
      if (!formData.username) {
        message.error('请输入用户名')
        setIsSubmitting(false)
        return
      }
      const usernameCheck = validateUsername(formData.username)
      if (!usernameCheck.valid) {
        message.error(usernameCheck.message)
        setIsSubmitting(false)
        return
      }
      if (!formData.password) {
        message.error('请输入密码')
        setIsSubmitting(false)
        return
      }
    } else {
      // 注册校验
      const usernameCheck = validateUsername(formData.username)
      if (!usernameCheck.valid) {
        message.error(usernameCheck.message)
        setIsSubmitting(false)
        return
      }
      const passwordCheck = validatePassword(formData.password)
      if (!passwordCheck.valid) {
        message.error(passwordCheck.message)
        setIsSubmitting(false)
        return
      }
      if (formData.password !== formData.confirmPassword) {
        message.error('两次输入的密码不一致')
        setIsSubmitting(false)
        return
      }
    }

    try {
      // 对密码进行 MD5 加密
      const encryptedPassword = md5(formData.password)
      
      if (authMode === 'login') {
        // 登录：使用用户名登录
        const res = await login({
          username: formData.username || undefined,
          password: encryptedPassword,
        }) as ApiResponse<LoginData>

        if (res.success) {
          message.success('登录成功')
          console.log('登录成功:', res.data)
          // TODO: 保存用户信息和 token，跳转到主页
        } else {
          message.error(res.message || '登录失败')
        }
      } else {
        // 注册
        const encryptedConfirmPassword = md5(formData.confirmPassword)
        const res = await register({
          username: formData.username,
          password: encryptedPassword,
          confirm_password: encryptedConfirmPassword,
        }) as ApiResponse<RegisterData>
        if (res.success) {
          message.success('注册成功')
          console.log('注册成功，用户ID:', res.data?.user_id)
          // 注册成功后切换到登录模式
          switchMode()
        } else {
          message.error(res.message || '注册失败')
        }
      }
    } catch (error: any) {
      message.error(error?.response?.data?.message || error?.message || '请求失败，请稍后重试')
    } finally {
      setIsSubmitting(false)
    }
  }

  const switchMode = () => {
    setAuthMode(prev => prev === 'login' ? 'register' : 'login')
    setFormData({
      username: '',
      password: '',
      confirmPassword: ''
    })
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: 'spring' as const,
        stiffness: 100,
        damping: 15
      }
    }
  }

  const formVariants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 100 : -100,
      opacity: 0
    }),
    center: {
      x: 0,
      opacity: 1
    },
    exit: (direction: number) => ({
      x: direction < 0 ? 100 : -100,
      opacity: 0
    })
  }

  // 密码显示切换按钮
  const passwordSuffix = (
    <button
      type="button"
      className="toggle-password"
      onClick={() => setShowPassword(!showPassword)}
    >
      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
    </button>
  )

  const confirmPasswordSuffix = (
    <button
      type="button"
      className="toggle-password"
      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
    >
      {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
    </button>
  )

  // 使用 useMemo 缓存随机值，避免每次渲染重新计算
  const backgroundElements = useMemo(() => ({
    stars: [...Array(30)].map((_, i) => ({
      id: i,
      left: `${(i * 3.3) % 100}%`,
      top: `${(i * 2.1) % 60}%`,
      size: 1 + (i % 3),
      delay: (i * 0.2) % 5,
      duration: 2 + (i % 3)
    })),
    meteors: [...Array(3)].map((_, i) => ({
      id: i,
      top: `${10 + i * 25}%`,
      left: `${-10 + i * 8}%`,
      delay: i * 6
    })),
    cloudsFar: [...Array(3)].map((_, i) => ({
      id: i,
      top: `${15 + i * 20}%`,
      width: 300 + i * 100,
      delay: i * 20
    })),
    cloudsMid: [...Array(3)].map((_, i) => ({
      id: i,
      top: `${25 + i * 22}%`,
      width: 400 + i * 80,
      delay: i * 15
    })),
    cloudsNear: [...Array(2)].map((_, i) => ({
      id: i,
      bottom: `${5 + i * 15}%`,
      width: 500 + i * 100,
      delay: i * 12
    })),
    spirits: [...Array(10)].map((_, i) => ({
      id: i,
      left: `${5 + i * 10}%`,
      size: 4 + (i % 4),
      delay: i * 1.2
    }))
  }), [])

  return (
    <div className="home-page">
      {/* 修仙世界背景动画 - 使用纯CSS动画优化性能 */}
      <div className="bg-animation">
        {/* 主渐变背景 */}
        <div className="bg-gradient"></div>

        {/* 星空层 - 减少数量，使用CSS动画 */}
        <div className="starfield">
          {backgroundElements.stars.map((star) => (
            <div
              key={`star-${star.id}`}
              className="star"
              style={{
                left: star.left,
                top: star.top,
                width: `${star.size}px`,
                height: `${star.size}px`,
                animationDelay: `${star.delay}s`,
                animationDuration: `${star.duration}s`
              }}
            />
          ))}
        </div>

        {/* 流星 - 使用CSS动画 */}
        <div className="meteors">
          {backgroundElements.meteors.map((meteor) => (
            <div
              key={`meteor-${meteor.id}`}
              className="meteor"
              style={{
                top: meteor.top,
                left: meteor.left,
                animationDelay: `${meteor.delay}s`
              }}
            />
          ))}
        </div>

        {/* 云海层 - 远景，使用CSS动画 */}
        <div className="cloud-layer cloud-far">
          {backgroundElements.cloudsFar.map((cloud) => (
            <div
              key={`cloud-far-${cloud.id}`}
              className="cloud cloud-far-item"
              style={{
                top: cloud.top,
                width: `${cloud.width}px`,
                animationDelay: `${cloud.delay}s`
              }}
            />
          ))}
        </div>

        {/* 云海层 - 中景 */}
        <div className="cloud-layer cloud-mid">
          {backgroundElements.cloudsMid.map((cloud) => (
            <div
              key={`cloud-mid-${cloud.id}`}
              className="cloud cloud-mid-item"
              style={{
                top: cloud.top,
                width: `${cloud.width}px`,
                animationDelay: `${cloud.delay}s`
              }}
            />
          ))}
        </div>

        {/* 云海层 - 近景 */}
        <div className="cloud-layer cloud-near">
          {backgroundElements.cloudsNear.map((cloud) => (
            <div
              key={`cloud-near-${cloud.id}`}
              className="cloud cloud-near-item"
              style={{
                bottom: cloud.bottom,
                width: `${cloud.width}px`,
                animationDelay: `${cloud.delay}s`
              }}
            />
          ))}
        </div>

        {/* 仙鹤飞行动画 - 使用CSS动画 */}
        <div className="immortal-crane">
          <div className="crane" style={{ top: '20%' }}>
            <div className="crane-body"></div>
            <div className="crane-wing left"></div>
            <div className="crane-wing right"></div>
          </div>
          <div className="crane crane-small crane-reverse" style={{ top: '35%' }}>
            <div className="crane-body"></div>
            <div className="crane-wing left"></div>
            <div className="crane-wing right"></div>
          </div>
        </div>

        {/* 灵气粒子 - 减少数量，使用CSS动画 */}
        <div className="spirit-particles">
          {backgroundElements.spirits.map((spirit) => (
            <div
              key={`spirit-${spirit.id}`}
              className="spirit-particle"
              style={{
                left: spirit.left,
                width: `${spirit.size}px`,
                height: `${spirit.size}px`,
                animationDelay: `${spirit.delay}s`
              }}
            />
          ))}
        </div>

        {/* 山脉剪影 */}
        <div className="mountain-silhouette">
          <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path
              className="mountain-back"
              d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,138.7C672,128,768,160,864,181.3C960,203,1056,213,1152,197.3C1248,181,1344,139,1392,117.3L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
            />
            <path
              className="mountain-front"
              d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,218.7C672,235,768,245,864,234.7C960,224,1056,192,1152,181.3C1248,171,1344,181,1392,186.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
            />
          </svg>
        </div>

        {/* 符文光晕 - 减少数量，使用CSS动画 */}
        <div className="rune-auras">
          {[...Array(4)].map((_, i) => (
            <div
              key={`aura-${i}`}
              className="rune-aura"
              style={{
                left: `${15 + i * 22}%`,
                top: `${25 + (i % 2) * 30}%`,
                animationDelay: `${i * 1.2}s`
              }}
            />
          ))}
        </div>
      </div>

      {/* 左侧修仙世界展示 */}
      <motion.div
        className="hero-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.2, ease: "easeOut" }}
      >
        {/* 背景装饰 - 飘动的仙气 */}
        <div className="hero-bg-effects">
          <div className="qi-flow qi-flow-1"></div>
          <div className="qi-flow qi-flow-2"></div>
          <div className="qi-flow qi-flow-3"></div>
        </div>

        <div className="hero-content">
          {/* 主图标 - 仙剑 */}
          <motion.div
            className="immortal-icon"
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ type: "spring", stiffness: 150, damping: 12, delay: 0.3 }}
          >
            <div className="icon-glow"></div>
            <Sword size={72} className="sword-icon" />
            <div className="icon-ring"></div>
            <div className="icon-ring delay-1"></div>
            <div className="icon-ring delay-2"></div>
          </motion.div>

          {/* 主标题 */}
          <motion.div
            className="title-wrapper"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <h1 className="hero-title">
              <span className="title-char" style={{ animationDelay: '0s' }}>仙</span>
              <span className="title-char" style={{ animationDelay: '0.1s' }}>途</span>
              <span className="title-char" style={{ animationDelay: '0.2s' }}>无</span>
              <span className="title-char" style={{ animationDelay: '0.3s' }}>疆</span>
            </h1>
            <div className="title-decoration">
              <span className="deco-line left"></span>
              <Sparkles size={20} className="deco-star" />
              <span className="deco-line right"></span>
            </div>
          </motion.div>

          {/* 副标题 */}
          <motion.p
            className="hero-tagline"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
          >
            <span className="tagline-text">踏破虚空 · 问道长生</span>
          </motion.p>

          {/* 修仙境界展示 */}
          <motion.div
            className="realm-showcase"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, duration: 0.6 }}
          >
            <div className="realm-track">
              {['炼气', '筑基', '金丹', '元婴', '化神', '渡劫', '大乘'].map((realm, index) => (
                <motion.div
                  key={realm}
                  className="realm-node"
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1.3 + index * 0.1, type: "spring", stiffness: 200 }}
                >
                  <div className="node-dot"></div>
                  <span className="node-label">{realm}</span>
                </motion.div>
              ))}
              <div className="track-line"></div>
            </div>
          </motion.div>

          {/* 特色卡片 */}
          <motion.div
            className="feature-cards"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.8 }}
          >
            <motion.div
              className="feature-card immortal"
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="card-icon flame">
                <Flame size={24} />
              </div>
              <div className="card-content">
                <h3>炼丹系统</h3>
                <p>采集天材地宝，炼制无上丹药</p>
              </div>
            </motion.div>

            <motion.div
              className="feature-card immortal"
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="card-icon star">
                <Star size={24} />
              </div>
              <div className="card-content">
                <h3>功法修炼</h3>
                <p>参悟天地玄机，习得无上神通</p>
              </div>
            </motion.div>
          </motion.div>
        </div>

        {/* 底部装饰符文 */}
        <div className="rune-decoration">
          {[...Array(5)].map((_, i) => (
            <motion.div
              key={i}
              className="rune"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 2 + i * 0.15, duration: 0.5 }}
            >
              {['道', '仙', '灵', '玄', '真'][i]}
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* 右侧登录/注册表单 */}
      <div className="auth-section">
        <div className="auth-container">
          {/* 切换标签 */}
          <div className="auth-tabs">
            <motion.button
              className={`tab ${authMode === 'login' ? 'active' : ''}`}
              onClick={() => authMode !== 'login' && switchMode()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              登录
              {authMode === 'login' && (
                <motion.div
                  className="tab-indicator"
                  layoutId="tabIndicator"
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
            </motion.button>
            <motion.button
              className={`tab ${authMode === 'register' ? 'active' : ''}`}
              onClick={() => authMode !== 'register' && switchMode()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              注册
              {authMode === 'register' && (
                <motion.div
                  className="tab-indicator"
                  layoutId="tabIndicator"
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
            </motion.button>
          </div>

          {/* 表单区域 */}
          <div className="form-wrapper">
            <AnimatePresence mode="wait" custom={authMode === 'login' ? 1 : -1}>
              <motion.form
                key={authMode}
                custom={authMode === 'login' ? 1 : -1}
                variants={formVariants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                onSubmit={handleSubmit}
                className="auth-form"
              >
                <div className="form-content">
                  {/* 用户名 */}
                  <motion.div
                    className="input-group"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                  >
                    <Input
                      placeholder="用户名"
                      value={formData.username}
                      onChange={handleInputChange('username')}
                      prefix={<User size={22} className="input-icon" />}
                      width="100%"
                      size="large"
                    />
                  </motion.div>

                  {/* 密码 */}
                  <motion.div
                    className="input-group"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                  >
                    <Input
                      type={showPassword ? 'text' : 'password'}
                      placeholder="密码"
                      value={formData.password}
                      onChange={handleInputChange('password')}
                      prefix={<Lock size={22} className="input-icon" />}
                      suffix={passwordSuffix}
                      width="100%"
                      size="large"
                    />
                  </motion.div>

                  {/* 注册时显示确认密码 */}
                  <AnimatePresence>
                    {authMode === 'register' && (
                      <motion.div
                        className="input-group"
                        initial={{ opacity: 0, height: 0, x: -20 }}
                        animate={{ opacity: 1, height: 'auto', x: 0 }}
                        exit={{ opacity: 0, height: 0, x: 20 }}
                        transition={{ type: "spring", stiffness: 300, damping: 30, delay: 0.1 }}
                      >
                        <Input
                          type={showConfirmPassword ? 'text' : 'password'}
                          placeholder="确认密码"
                          value={formData.confirmPassword}
                          onChange={handleInputChange('confirmPassword')}
                          prefix={<Lock size={22} className="input-icon" />}
                          suffix={confirmPasswordSuffix}
                          width="100%"
                          size="large"
                        />
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* 登录时的忘记密码 */}
                  {authMode === 'login' && (
                    <motion.div
                      className="form-options"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                    >
                      <label className="remember-me">
                        <input type="checkbox" />
                        <span>记住我</span>
                      </label>
                      <a href="#" className="forgot-password">忘记密码?</a>
                    </motion.div>
                  )}

                  {/* 提交按钮 */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                  >
                    <Button
                      variant="primary"
                      size="large"
                      loading={isSubmitting}
                      htmlType="submit"
                      className="submit-btn"
                    >
                      {authMode === 'login' ? '登 录' : '立即注册'}
                    </Button>
                  </motion.div>
                </div>
              </motion.form>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  )
}
